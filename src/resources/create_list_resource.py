import random

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
        self._bad_list = [
            Texts(
                'Плохой список.',
                'Ваш ввод не похож на список в требуемом формате'
            ),
            Texts(
                'Плохой список.',
                'Я Вас просила немецкие слова пополам с русскими, а Вы мне манную кашу пополам с малиновым вареньем.'
            ),
            Texts(
                'Плохой список.',
                'Список - не фонтан. Уверена, Вы можете лучше.'
            ),
            Texts(
                'Плохой список.',
                'Что то пошло не так, список распознать не удалось.'
            ),
            Texts(
                'Плохой список.',
                'Этот список плохо отразился на моём пищеварении. Хочу другой.'
            )
        ]

    def bad_list(self):
        variant = self._bad_list[random.randrange(len(self._bad_list))]

        return variant.text(), variant.tts()
