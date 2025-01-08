import os
import torch


class Silero:
    ru_16 = {
        'url': 'https://models.silero.ai/models/tts/ru/v2_kseniya.pt',
        'rate': 16000,
        'file_name': 'model_ru_16.pt'
    }
    de_16 = {
        'url': 'https://models.silero.ai/models/tts/de/v2_thorsten.pt',
        'rate': 16000,
        'file_name': 'model_de_16.pt'
    }

    def __init__(self, variant):
        self.path = os.path.dirname(__file__)
        device = torch.device('cpu')
        torch.set_num_threads(4)
        local_file = os.path.join(os.path.dirname(__file__), variant['file_name'])
        self.rate = variant['rate']
        if not os.path.isfile(local_file):
            torch.hub.download_url_to_file(variant['url'], local_file)

        model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
        model.to(device)
        self.model = model

    def get_audio(self, text):
        def audio(path):
            with open(path, 'rb') as file:
                data = file.read()
            # if os.path.exists(path):
            #     os.remove(path)
            return data

        texts = text if isinstance(text, list) else [text]
        audio_paths = self.model.save_wav(texts=texts,
                                          sample_rate=self.rate,
                                          )
        result = [audio(path) for path in audio_paths]
        return result


def silero(word, variant=None):
    if variant is None:
        variant = Silero.de_16
    path = os.path.dirname(__file__)
    # audio_path = os.path.join(path, "audio", f'{word.replace(' ', '_')}.wav')
    device = torch.device('cpu')
    torch.set_num_threads(4)
    local_file = os.path.join(path, variant['file_name'])
    rate = variant['rate']
    if not os.path.isfile(local_file):
        torch.hub.download_url_to_file(variant['url'], local_file)

    model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
    model.to(device)
    audio_paths = model.save_wav(texts=[word],
                                 sample_rate=rate,
                                 )
    with open(audio_paths[0], 'rb') as file:
        data = file.read()
    # with open(audio_path, 'wb') as file:
    #     file.write(data)
    if os.path.exists(audio_paths[0]):
        os.remove(audio_paths[0])
    return data


if __name__ == '__main__':
    print('Silero')
    # silero_ru = Silero(Silero.ru_16)
    # print(silero_ru.get_audio('М+ама М+илу м+ыла с м+ылом.'))
    # silero_de = Silero(Silero.de_16)
    print(silero('das Buch'))
    print(silero('das Fahrrad'))
