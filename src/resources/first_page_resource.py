from resources.resource import Resource
from resources.texts import Texts


class UserType:
    def __init__(self, old, new):
        self.old = old
        self.new = new


class First(Resource):
    def __init__(self):
        super().__init__()
        text_exit = 'Для выхода из навыка, скажите,   Бюргер, закройся.'
        self.greeting = UserType(
            Texts(
                'Рада снова вас видеть. Давайте продолжим изучать немецкие слова и выражения.'
                ' Хотите выбрать существующий список или создать новый?', ''
            ),
            Texts(
                'Добро пожаловать в режим тренировки слов и выражений на немецком языке.'
                ' Здесь я помогу вам потренировать и запомнить слова, которые вы хотели бы выучить.'
                ' Но прежде, вам необходимо продиктовать слова или фразы и их значения, чтобы я создала список,'
                ' по которому буду вас тренировать.   Начнём?', '')
        )
        self.create_list = Texts(
            'Создаю список слов: "{}" '
            'Введите список слов, (словосочетаний) в формате <немецкое слово> <разделитель> <перевод>.'
            ' В качестве разделителя используйте ":" или "-", в качестве разделителя элементов (строк)'
            ' списка - символ перевода строки. Строки длиннее 64 символов будут отброшены',
            'Создаю список слов.   {} sil<[100]>'
            'Введите построчно через дефис немецкие слова и их перевод.'
        )

        text = 'Фраза "{}" не понятна мне. '
        tts_new = ('Для создания нового списка скажите,  создай новый список, и имя списка.'
                   '  В качестве названия, годится любая фраза, не длиннее двух слов.')

        self._no_command = UserType(
            Texts(
                text + 'Доступные команды: \n'
                       '\t"Создай новый список + [Имя списка]"'
                       '\t"Выбери список + <Имя списка из максимум двух слов>"'
                       '\t"Покажи мои списки"',
                text + tts_new + '  Для выбора существующего списка скажите, выбери список и назовите имя списка. '
                + text_exit
            ),
            Texts(text, text + tts_new + text_exit)
        )

        self.quest_list_name = Texts(
            'Как будет называться ваш список слов?', ''
        )

        self._intents = UserType(
            ['START', 'NEW', 'SHOW', 'SELECT_LIST', 'HELP', 'WHAT_CAN'],
            ['NEW', 'YES', 'HELP', 'WHAT_CAN']
        )

        self._cards = UserType(
            ['START', 'NEW', 'SHOW'],
            ['NEW']
        )

    def no_command(self, is_old):
        return self._no_command.old if is_old else self._no_command.new

    def intents(self, is_old):
        return self._intents.old if is_old else self._intents.new

    def cards(self, is_old):
        return self._cards.old if is_old else self._cards.new

    # def check_command(self, command, is_old=True):
    #     commands = self._intents.old if is_old else self._intents.new
    #     return command if command in commands else 'NO_COMMAND'

    def get_greeting(self, is_old):
        text = self.greeting.old.text() if is_old else self.greeting.new.text()
        tts = self.greeting.old.tts() if is_old else self.greeting.new.tts()
        return text, tts

    def get_no_command(self, is_old):
        text = self._no_command.old.text() if is_old else self._no_command.new.text()
        tts = self._no_command.old.tts() if is_old else self._no_command.new.tts()
        return text, tts
