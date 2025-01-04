import os
import torch


if __name__ == '__main__':
    device = torch.device('cpu')
    torch.set_num_threads(4)
    local_file = 'model.pt'

    if not os.path.isfile(local_file):
        torch.hub.download_url_to_file('https://models.silero.ai/models/tts/ru/v2_kseniya.pt',
                                       local_file)

    model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
    model.to(device)

    example_batch = ['В недрах тундры выдры в г+етрах т+ырят в вёдра ядра к+едров.',
                     'Котики - это жидкость!',
                     'М+ама М+илу м+ыла с м+ылом.']
    sample_rate = 16000
    print(os.path.join(os.path.dirname(__file__), 'wav'))
    audio_paths = model.save_wav(texts=example_batch,
                                 sample_rate=sample_rate,
                                 )
