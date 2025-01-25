from resources.resource import Resource
from resources.texts import Texts


class Question(Resource):
    def __init__(self):
        super().__init__()
        self._intents = ['SKIP', 'STOP', 'HELP']
        self._select_hint = Texts(
            'Какая Вам нужна подсказка? Или пропустить слово?',
            'Какая Вам нужна подсказка? Или пропустить слово?'
        )
        self._stop = Texts(
            'Завершаем тренинг. Что делаем дальше?',
            'Завершаем тренинг. Что делаем дальше?'
        )
        self._help = Texts(
            '''
            Вы можете назвать перевод, пропустить слово, или прекратить тренинг.
            Вам доступны подсказки: "Дай синоним", "Подскажи первый слог" 
            ''',
            '''
            Вы можете назвать перевод, пропустить слово, или прекратить тренинг.
            Вам доступны подсказки: "Дай синоним", "Подскажи первый слог" 
            '''
        )

    def select_hint(self):
        return (self._select_hint.text(),
                f'<{self.speaker}/{self.skil}/{self.fail}.opus"> sil <[{self.sil}]> {self._select_hint.tts()}')

    def stop(self):
        return self._stop.text(), self._stop.tts()
