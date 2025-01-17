import json
import os.path
import time
from pathlib import Path

import jwt
import requests
from datetime import datetime

import ydb


class YdbBase:
    aud = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
    keys_file = os.path.join(os.path.dirname(__file__), 'authorized_key.json')
    endpoint = 'grpcs://ydb.serverless.yandexcloud.net:2135'
    base = '/ru-central1/b1g8c46f4fkf6jlpdg5n/etniis25oq2u6jasijmh'
    sql = Path.joinpath(Path(__file__).parents[2], "sql")
    create = Path.joinpath(sql, "create_tables.sql")
    drop = Path.joinpath(sql, "drop_tables.sql")
    clear = Path.joinpath(sql, "clear_tables.sql")

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
            file = f.read()
            obj = json.loads(file)
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

    def insert_audio(self, word, file_name):
        return self.pool.execute_with_retries(
            f"""
                INSERT INTO audio (de, file_path) 
                VALUES ('{word}', '{file_name}');
            """,
        )[0]

    def insert_new_words(self, words):
        values = ', '.join(list(map(
            lambda item: f"(CurrentUtcDatetime(), CurrentUtcDatetime(), Utf8('{item[0]}'), Utf8('{item[1]}'))", words)))
        return self.pool.execute_with_retries(
            f"""
                INSERT INTO words (de, ru, expire_at, updated_on)
                    SELECT l.de as de, l.ru as ru, l.expire as expire_at, l.updated as updated_on
                    FROM words
                    RIGHT JOIN
                        (SELECT DISTINCT * FROM
                        (VALUES {values}) AS X(expire, updated, de, ru)) as l
                    ON (words.de = l.de AND words.ru = l.ru)
                    WHERE id ISNULL
                RETURNING id, de;
            """,
        )[0]

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

        head = tx.execute(
            f"""INSERT INTO user_words (word_id, list_id)
                    SELECT id as word_id, {list_id} as list_id
                    FROM words
                    INNER JOIN
                        (SELECT DISTINCT * FROM
                        (VALUES {values}) AS X(de, ru))
                        as l
                    ON (words.de = l.de AND words.ru = l.ru)
                RETURNING word_id;""")[0].rows[:3]
        tx.commit()
        return list_id, head

    def select_without_file(self, words):
        values = ', '.join(list(map(lambda item: f"({item['id']}, Utf8('{item['de']}'))", words)))
        print('values', values)
        return self.pool.execute_with_retries(
            f"""
                SELECT l.id as id, l.de as de FROM audio 
                RIGHT JOIN  
                    (SELECT DISTINCT id, de FROM
                    (VALUES {values}) AS X(id, de)) as l
                ON audio.de = l.de
                WHERE file_path ISNULL;     
            """)[0].rows

    def select_lists(self, user):
        user_id = self.insert_user(user).rows[0].id
        lists = self.pool.execute_with_retries(f"SELECT id, name FROM user_lists WHERE user_id = {user_id};", )
        return lists[0].rows, user_id

    def get_list_id(self, user, name):
        res = self.pool.execute_with_retries(f"""
        SELECT id, is_loaded FROM user_lists WHERE user_id in 
            (SELECT id FROM users WHERE name = '{user}')
            AND name = '{name}';""", )[0].rows
        return (False, False) if not res else (res[0].id, res[0].is_loaded)

    def select_free_names(self, names):
        values = ', '.join(list(map(lambda name: f"('{name}')", names))) if names else "('')"
        result = self.pool.execute_with_retries(f"""
        SELECT name FROM (SELECT DISTINCT * FROM
            (VALUES {values}) AS X(color))
            as l
            RIGHT JOIN colors
            ON l.color = colors.name
            WHERE color ISNULL
        """)
        return [row.name for row in result[0].rows]

    def select_words_list(self, list_id):
        res = self.pool.execute_with_retries(f"""
        SELECT ru, de, file_path, ids.id as id, audio_id FROM words 
        RIGHT JOIN 
            (SELECT word_id as id, audio_id FROM user_words WHERE list_id = {list_id}) as ids
        ON words.id = ids.id;    
                """, )
        return res[0].rows

    def set_audio_id(self, *args):
        query_text = f"""
            UPDATE user_words SET audio_id = '{args[1]}' WHERE id = {args[0]} RETURNING id;
        """ if len(args) == 2 else f"""
            UPDATE user_words SET audio_id = '{args[2]}' WHERE word_id = {args[0]} AND list_id = {args[1]} RETURNING id;
        """

        res = self.pool.execute_with_retries(query_text)[0].rows
        return res[0].id == id if res else False

    def get_file_path(self, word):
        return self.pool.execute_with_retries(
            f"SELECT file_path FROM audio WHERE de = '{word}';",
        )[0]

    def get_added_words(self, list_id):
        return self.pool.execute_with_retries(
            f"SELECT id, audio_id FROM user_words WHERE list_id = '{list_id}' AND is_processed ISNULL;",
        )[0]

    def get_words_by_id(self, ids):
        value = f"( {', '.join(ids)} )"
        return self.pool.execute_with_retries(
            f"SELECT id, de FROM words WHERE id IN {value};",
        )[0].rows

    def get_list_is_loaded(self, id):
        res = self.pool.execute_with_retries(
            f"SELECT id, is_loaded FROM user_lists WHERE id = {id};"
        )[0].rows
        return (res[0].id, res[0].is_loaded) if res else (None, None)

    def set_list_is_loaded(self, id, is_loaded):
        res = self.pool.execute_with_retries(f"""
            UPDATE user_lists SET is_loaded = {is_loaded} WHERE id = {id} RETURNING id, is_loaded;
        """)[0].rows
        print(res)
        return (res[0].id, res[0].is_loaded) if res else (None, None)

    def reset_list_is_loaded(self, list_id):
        tx = self.session.transaction().begin()
        tx.execute(
            f"UPDATE user_words SET audio_id = NULL WHERE list_id = {list_id};"
        )
        tx.execute(
            f"UPDATE user_lists SET is_loaded = NULL WHERE id = {list_id};"
        )
        tx.commit()

    def select_all_audio(self):
        return self.pool.execute_with_retries(
            f"SELECT audio_id FROM user_words WHERE audio_id NOTNULL;",
        )[0].rows

    def exec_file(self, fn):
        with open(fn, 'r') as f:
            query = f.read()
        self.pool.execute_with_retries(query)

    def create_tables(self):
        self.exec_file(YdbBase.create)

    def drop_tables(self):
        self.exec_file(YdbBase.drop)

    def clear_tables(self):
        self.exec_file(YdbBase.clear)

    def insert_color(self, values):
        return self.session.transaction().execute(
            f"REPLACE INTO colors (name, hex) "
            f"VALUES {values};"
        )


if __name__ == '__main__':
    base = YdbBase()
    # base.drop_tables()
    # base.create_tables()
    # id = base.get_list_id("EFE76D1449413314CDB750CCB4D3562A2F85DB599A5A465E98C494888474FE13", "Майский зеленый")
    # print(id)
    # id = base.get_list_id("EFE76D1449413314CDB750CCB4D3562A2F85DB599A5A465E98C494888474FE13", "Майский")
    # print(id)
    # words = base.select_words_list(1)
    # print(words)
    # res = base.set_audio_id(1, 'audio_id')
    # id, is_loaded = base.get_list_is_loaded(3)
    # print(id, is_loaded)
    # res = base.set_list_is_loaded(1, False)
    # print(res)
    # base.reset_list_is_loaded(1)
