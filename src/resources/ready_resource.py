from load_resource.load_audio import LoadAudio
from resources.resource import Resource
from resources.texts import Texts


class Ready(Resource):
    def __init__(self):
        super().__init__()
        self._intents = ['YES', 'NO', 'START']
        self._end_list = Texts(
            'Поздравляю, вы выучили весь список слов и выражений!'
            ' Закрепим полученные знания? Или потренируем другие списки слов?',
            'Поздравляю, вы выучили весь список слов и выражений! sil <[{}]> '
            'Закрепим полученные знания? Или потренируем другие списки слов?'
        )
        self._dont_understand = Texts(
            'Ваша фраза {}, означает "ДА?" или "НЕТ?"',
            'Ваша фраза {}, означает, "ДА?", или, "НЕТ?"',
        )
        self._question = Texts(
            '{}: {}', ''
        )
        self._start = Texts(
            '', 'Начинаем тренинг. Правила простые. Я Вам - слово. Вы мне перевод. sil <[{}]> '
        )

    def grade(self, excellent):
        return '' if excellent is None\
            else f'<{self.speaker}/{self.skil}/{self.excellent if excellent else self.fail}.opus"> sil <[{self.sil}]>'

    def question(self, word, excellent):
        audio = f'<{self.speaker}/{self.skil}/{word['audio_id']}.opus">'
        return self._question.text(word['de'], word['ru']), f'{self.grade(excellent)} {audio}'

    def end_list(self):
        return self._end_list.text(), self._end_list.tts(self.sil)

    def start(self):
        return self._start.tts(self.sil)

    def dont_understand(self, word):
        return self._dont_understand.text(word), self._dont_understand.tts(word)
