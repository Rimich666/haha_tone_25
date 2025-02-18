from resources.resource import Resource
from resources.texts import Texts


class NameSelectList(Resource):
    def __init__(self):
        super().__init__()
        self._intents = ['YES', 'NO']
        self.list_select = Texts(
            'Какой список Вы хотите выбрать?',
            'Какой список Вы хотите выбрать?'
        )
        self.dont_understand = Texts(
            'Ваша фраза {}, означает "ДА?" или "НЕТ?"',
            'Ваша фраза {}, означает, "ДА?", или, "НЕТ?"',
        )
        self.no_lists = Texts(
            'Нет у Вас списков',
            'Нет у Вас списков'
        )
        self.offers = [
            Texts('Хотите выбрать список {}?', 'Хотите выбрать список {}?'),
            Texts('Может список {}?', 'Может список {}?'),
            Texts('Выберем список {}?', 'Выберем список {}?'),
            Texts('Давайте выберем список {}', 'Давайте выберем список {}'),
            Texts('Предлагаю выбрать {}', 'Предлагаю выбрать {}')
        ]
        self.end_names = Texts('Всё, списков больше нет.', 'Всё, списков больше нет.')
        self.no_list = Texts(
            'Списка {}, не существует. ',
            'Списка {}, не существует. ',
        )
        self._help = Texts(
            '',
            'Вы можете назвать имя списка. Можете сказать: "Выбери автоматически",'
            ' Можете согласится, или отклонить выбранное имя.'
            ' Если решение не будет принято - имя списка будет выбрано автоматически'
        )
