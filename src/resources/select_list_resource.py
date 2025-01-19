from resources.resource import Resource
from resources.texts import Texts


class SelectList(Resource):
    def __init__(self):
        super().__init__()
        self._intents = ['AGAIN', 'RESUME']
        self.ready = Texts(
            'Список {} готов к работе. Начать тренинг?', 'Список {} готов к работе. Начать тренинг?'
        )
        self.full_or_not = Texts(
            'В списке {} вы выучили {} {} из {}. Хотите продолжить изучение или начать заново?',
            'В списке {} вы выучили {} {} из {}. Хотите продолжить изучение или начать заново?'
        )
        self.whatever = Texts(
            'Вы сказали {}. Я думаю это значит, что Вы хотите начать с начала. ',
            'Вы сказали {}. Я думаю это значит, что Вы хотите начать с начала. sil<[500]>'
        )
