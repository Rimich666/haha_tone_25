from resources.resource import Resource
from resources.texts import Texts


class CreateList(Resource):
    def __init__(self):
        super().__init__()
        self._intents = []
        self.list_created = Texts(
            'Список "{}" готов к работе. Выбрать его для тренинга?',
            'Список {} готов к работе. sil <[1500]> Хотите выбрать его для начала тренинга?'
        )
