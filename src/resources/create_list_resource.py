from resources.resource import Resource
from resources.texts import Texts


class CreateList(Resource):
    def __init__(self):
        super().__init__()
        self._intents = ['HELP']
        self.list_created = Texts(
            'Список "{}" создан. Выбрать его для тренинга?',
            'Список {} создан. sil <[1500]> Хотите выбрать его для начала тренинга?'
        )
