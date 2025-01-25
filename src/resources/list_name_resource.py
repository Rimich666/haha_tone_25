from resources.resource import Resource
from resources.texts import Texts


class ListName(Resource):
    def __init__(self):
        super().__init__()
        self.check = Texts(
            'Вы хотите назвать список: "{}"?',
            'Вы хотите назвать список.  {}?')
        self._intents = ['AUTO', 'YES', 'NO', 'HELP']
        sil = 170
        self.extents = [
            Texts('', f'С первой попытки не всегда удаётся правильно назвать список. sil<[{sil}]>'
                      ' Так как, назовём список?'),
            Texts('', f'Вторая попытка тоже не всегда бывает удачной. sil<[{sil}]> Придумайте новое название.'),
            Texts('', f'Бог конечно любит троицу,   но и четыре попытки ещё не конец. sil<[{sil}]>'
                      ' Можете назвать как, душе угодно.'),
            Texts('', f'Ну что же, так тоже бывает. sil<[{sil}]> Попробуйте ещё раз.'),
            Texts('Вы всё ещё хотите создать список слов?', 'Вы всё ещё хотите создать список слов?'),
        ]
        self._help = Texts(
            '''Доступные команды: 
                "Выбери автоматически."
                "Да."
                "Нет."
                "Помощь"
                ''',
            f'''Вы можете назвать имя списка. Можете сказать: "Выбери автоматически",'
            ' Можете согласится, или отклонить выбранное имя.'
            ' Если решение не будет принято - имя списка будет выбрано автоматически sil<[{sil}]>'''
        )

    def mode(self):
        return self._intents

    # def check_command(self, command):
    #     commands = self._intents
    #     return command if command in commands else 'NO_COMMAND'
