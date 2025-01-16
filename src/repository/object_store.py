import boto3


class ObjectStore:
    url = 'https://storage.yandexcloud.net:'
    ydb_folder = 'b1g6tcs69ql56gorgahs'
    bucket_name = 'hahaaudio'

    def __init__(self):
        self.session = boto3.session.Session()
        self.s3 = self.session.client(
            service_name='s3',
            endpoint_url=ObjectStore.url
        )

    def upload_file(self, path, file_name):
        self.s3.upload_file(path, self.bucket_name, file_name)

    def get_object(self, key):
        response = self.s3.get_object(Bucket=self.bucket_name, Key=key)
        return response['Body'].read()

    def get_list(self):
        response = self.s3.list_objects(Bucket=self.bucket_name).get('Contents', [])
        return response

    def upload_string(self, key, body):
        self.s3.put_object(Bucket=self.bucket_name, Key=key, Body=body)

    def delete(self):
        records = list(map(lambda item: {'Key': item['Key']}, self.get_list()))
        response = self.s3.delete_objects(Bucket=self.bucket_name, Delete={'Objects': records})
        return response

    def delete_by_key(self, key):
        response = self.s3.delete_object(Bucket=self.bucket_name, Key=key)
        return response


if __name__ == '__main__':
    print('object storage')
    store = ObjectStore()
    store.get_list()
