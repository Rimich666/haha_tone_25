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

    def select_user(self, name):
        return self.session.transaction().execute(
            f"SELECT id, name FROM users WHERE name = '{name}';",
            commit_tx=True
        )

    def insert_user(self, name):
        user = self.select_user(name)
        if user[0].rows:
            return user
        return self.session.transaction().execute(
            f"INSERT INTO users (expire_at, updated_on, name) "
            f"VALUES (CurrentUtcDatetime(), CurrentUtcDatetime(), '{name}') RETURNING id, name;",
            commit_tx=True
        )

    def select_word(self, ru, de):
        return self.session.transaction().execute(
            f"SELECT id, ru, de FROM words WHERE ru = '{ru}' and de = '{de}';",
            commit_tx=True
        )

    def insert_word(self, ru, de):
        word = self.select_word(ru, de)
        if word[0].rows:
            return word
        return self.session.transaction().execute(
            f"INSERT INTO words (expire_at, updated_on, ru, de) "
            f"VALUES (CurrentUtcDatetime(), CurrentUtcDatetime(), '{ru}', '{de}') RETURNING id, ru, de;"
        )

    def add_word(self, ru, de, user):
        user = self.insert_user(user)
        word = self.insert_word(ru, de)
        print(word[0].rows[0]['id'], user[0].rows[0]['id'])

