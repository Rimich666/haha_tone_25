import json
import requests

from repository.object_store import ObjectStore


class LoadAudio:
    oauth_key = 'oauth_key.json'
    host = 'https://dialogs.yandex.net'

    def __init__(self):
        with open(LoadAudio.oauth_key, 'r') as f:
            file = f.read()
            obj = json.loads(file)
            self.token = obj['key']
            self.skill = obj['id']
        self.store = ObjectStore()
        pass

    def get_limit(self):
        response = requests.get(f'{self.host}/api/v1/status', headers={'Authorization': f'OAuth {self.token}'})
        print(response.json())

    def load_file(self, file_name):
        audio = self.store.get_object(file_name)
        response = requests.post(
            f'{self.host}/api/v1/skills/{self.skill}/sounds',
            headers={'Authorization': f'OAuth {self.token}'},
            files={'file': audio}
        )
        return response.json()['sound']['id']

    def get_status(self, id):
        response = requests.get(
            f'{self.host}/api/v1/skills/{self.skill}/sounds/df284827-c4ae-4187-8dae-d046c378e578',
            headers={'Authorization': f'OAuth {self.token}'})
        print(response.json())


if __name__ == '__main__':
    load_audio = LoadAudio()
    load_audio.get_limit()
    print(load_audio.store.get_list())
    # audio_id = load_audio.load_file('zwanzig.wav')
    load_audio.get_status('840d6d27-a193-4de8-ab81-8588e657525d')
    # 'df284827-c4ae-4187-8dae-d046c378e578'