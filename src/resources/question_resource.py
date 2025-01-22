from resources.resource import Resource
from resources.texts import Texts


class Question(Resource):
    def __init__(self):
        super().__init__()
        self._intents = ['SKIP', 'STOP']
        self._select_hint = Texts(
            'Какая Вам нужна подсказка? Или пропустить слово?',
            'Какая Вам нужна подсказка? Или пропустить слово?'
        )

    def select_hint(self):
        return (self._select_hint.text(),
                f'<{self.speaker}/{self.skil}/{self.fail}.opus"> sil <[{self.sil}]> {self._select_hint.tts()}')
