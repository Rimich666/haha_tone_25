from resources.resource import Resource
from resources.texts import Texts


class EndList(Resource):
    def __init__(self):
        super().__init__()
        self._intents = ['NO', 'FIX', 'ANOTHER']
        self._back = Texts(
            'Вы закончили обучение.',
            'Что будем делать дальше?'
        )
        self._not_understand = Texts(
            'Вы закончили обучение.',
            '''Не понимаю что значит {}, думаю, это значит, нет. sil<[1500]>
                Что будем делать дальше?'''
        )

    def back(self):
        return self._back.text(), self._back.tts()

    def not_understand(self, original):
        return self._back.text(), self._back.tts(original)
