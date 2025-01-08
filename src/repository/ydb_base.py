import json
import os.path
import time
import jwt
import requests
from datetime import datetime

import ydb


class YdbBase:
    aud = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
    keys_file = os.path.join(os.path.dirname(__file__), 'authorized_key.json')
    endpoint = 'grpcs://ydb.serverless.yandexcloud.net:2135'
    base = '/ru-central1/b1g8c46f4fkf6jlpdg5n/etniis25oq2u6jasijmh'

    def __init__(self):
        self.session = None
        self.pool = None
        self.driver = None
        self.iam = ''
        self.token = ''
        self.expires = 0
        self.create_jwt_token()
        self.create_IAM()
        self.init_driver()

    def create_jwt_token(self):
        # Чтение закрытого ключа из JSON-файла
        with open(YdbBase.keys_file, 'r') as f:
            obj = f.read()
            obj = json.loads(obj)
            private_key = obj['private_key']
            key_id = obj['id']
            service_account_id = obj['service_account_id']

        now = int(time.time())
        payload = {
            'aud': YdbBase.aud,
            'iss': service_account_id,
            'iat': now,
            'exp': now + 3600
        }

        # Формирование JWT.
        encoded_token = jwt.encode(
            payload,
            private_key,
            algorithm='PS256',
            headers={'kid': key_id}
        )

        self.token = encoded_token

    def create_IAM(self):
        resp = requests.post(YdbBase.aud, headers={'Content-Type': 'application/json'},
                             data=json.dumps({'jwt': self.token})).json()
        self.iam = resp['iamToken']
        self.expires = datetime.fromisoformat(resp['expiresAt']).timestamp()

    def init_driver(self):
        self.driver = ydb.Driver(
            endpoint=YdbBase.endpoint,
            database=YdbBase.base,
            credentials=ydb.AccessTokenCredentials(self.iam),
        )
        self.driver.wait(timeout=5)
        self.session = self.driver.table_client.session().create()
        self.pool = ydb.QuerySessionPool(self.driver)

    def select_user(self, name):
        return self.pool.execute_with_retries(
            f"SELECT id, name FROM users WHERE name = '{name}';",
        )[0]

    def insert_user(self, name):
        user = self.select_user(name)
        print('insert:', user)
        if user.rows:
            return user
        return self.pool.execute_with_retries(
            f"""
                INSERT INTO users (expire_at, updated_on, name) 
                VALUES (CurrentUtcDatetime(), CurrentUtcDatetime(), '{name}') RETURNING id, name;
            """,
        )[0]

    def select_word(self, ru, de):
        return self.session.transaction().execute(
            f"SELECT id, ru, de FROM words WHERE ru = '{ru}' and de = '{de}';",
            commit_tx=True
        )

    def insert_word(self, ru, de, audio):
        word = self.select_word(ru, de)
        if word[0].rows:
            return word
        return self.pool.execute_with_retries(
            f"INSERT INTO words (expire_at, updated_on, ru, de, file_path) "
            f"VALUES (CurrentUtcDatetime(), CurrentUtcDatetime(), '{ru}', '{de}', '{audio}') RETURNING id, ru, de;"
        )

    def insert_color(self, values):
        return self.session.transaction().execute(
            f"REPLACE INTO colors (name, hex) "
            f"VALUES {values};"
        )

    def add_word(self, ru, de, user):
        user = self.insert_user(user)
        word = self.insert_word(ru, de)
        print(word[0].rows[0]['id'], user[0].rows[0]['id'])

    def create_list(self, words, user, name):
        values = ', '.join(list(map(lambda item: f"('{item[0]}', '{item[1]}')", words)))
        tx = self.session.transaction().begin()

        list_id = tx.execute(
            f"""
            INSERT INTO user_lists (expire_at, updated_on, user_id, name) 
                VALUES  (CurrentUtcDatetime(), CurrentUtcDatetime(), {user}, '{name}')
                RETURNING id;
            """
        )[0].rows[0]['id']

        all_res = tx.execute(
            f"""INSERT INTO user_words (word_id, list_id)
                    SELECT id as word_id, {list_id} as list_id
                    FROM words
                    INNER JOIN
                        (SELECT DISTINCT * FROM
                        (VALUES {values}) AS X(de, ru))
                        as l
                    ON (words.de = l.de AND words.ru = l.ru)
                RETURNING id;""")
        tx.commit()
        return all_res[0].rows

    def select_new_words(self, words):
        values = ', '.join(list(map(lambda item: f"({item[0]}, '{item[1][0]}', '{item[1][1]}')", enumerate(words))))
        new_res = self.pool.execute_with_retries(
            f"""SELECT new_words.de as de, new_words.ru as ru, new_words.index as index, words.file_path as file 
            FROM (SELECT de, ru, index FROM (SELECT words.de as base, l.de as de, l.ru as ru, l.index as index
                FROM words
                RIGHT JOIN
                    (SELECT DISTINCT * FROM
                        (VALUES {values}) AS X(index, de, ru))
                    as l
                ON (words.de = l.de AND words.ru = l.ru)) as list_words
                WHERE list_words.base ISNULL) as new_words
            LEFT JOIN words
            ON new_words.de = words.de;"""
        )

        return [(
            row.de.decode('utf8'),
            row.ru.decode('utf8'),
            row.file,
            row.index) for row in new_res[0].rows]

    def select_lists(self, user):
        user_id = self.insert_user(user).rows[0].id
        lists = self.pool.execute_with_retries(f"SELECT id, name FROM user_lists WHERE user_id = {user_id};",)
        print(lists)
        return lists[0].rows, user_id

    def select_free_names(self, names):
        values = ', '.join(list(map(lambda name: f"('{name}')", names)))
        result = self.pool.execute_with_retries(f"""
        SELECT name FROM (SELECT DISTINCT * FROM
            (VALUES {values}) AS X(color))
            as l
            RIGHT JOIN colors
            ON l.color = colors.name
            WHERE color ISNULL
        """)
        return [row.name for row in result[0].rows]
