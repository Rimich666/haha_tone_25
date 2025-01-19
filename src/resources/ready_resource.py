from load_resource.load_audio import LoadAudio
from resources.resource import Resource
from resources.texts import Texts


class Ready(Resource):
    def __init__(self):
        super().__init__()
        self._intents = ['YES', 'NO', 'START']
        self.skil = LoadAudio.get_skil()[0]
        self.speaker = 'speaker audio="dialogs-upload'
        self.excellent = '874c6dcf-c804-4d1a-aa5f-e80ac9aad43c'
        self.fail = '6fa4bf54-54e3-4b18-9f41-352112d51b42'
        self.sil = 700
        self._end_list = Texts(
            'Поздравляю, вы выучили весь список слов и выражений! Хотите потренировать слова из других списков?',
            'Поздравляю, вы выучили весь список слов и выражений! sil <[{}]> '
            'Хотите потренировать слова из других списков?'
        )
        self._question = Texts(
            '{}: {}', ''
        )
        self._start = Texts(
            '', 'Начинаем тренинг. Правила простые. Я Вам - слово. Вы мне перевод. sil <[{}]> '
        )

    def grade(self, excellent):
        return '' if excellent \
            else f'<{self.speaker}/{self.skil}/{self.excellent if excellent else self.fail}.opus"> sil <[{self.sil}]>'

    def question(self, word, excellent):
        audio = f'<{self.speaker}/{self.skil}/{word['audio_id']}.opus">'
        return self._question.text(word['de'], word['ru']), f'{self.grade(excellent)} {audio}'

    def end_list(self):
        return self._end_list.text(), self._end_list.tts(self.sil)

    def start(self):
        return self._start.tts(self.sil)
