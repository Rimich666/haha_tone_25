DICT_API_KEY = 'dict.1.1.20241230T092206Z.ba9a5db11c2aadec.8888be2957feb67ffbe9ab39f37a7812c9de1615'
DICT_URL = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup'

check_images = {
    True: '1030494/aeaac6f5e4866ee83eaf',
    False: '1540737/3767a411c46814372595'
}

"""
    Стартовое сообщение
"""

mode_images = {
    'NEW': '1540737/a0df801b838190067c9d',
    'START': '965417/307b56a1df136b4784bb',
    'SHOW': '937455/1ef159a26459009bdeb0'
}

descriptions = {
    'START_TEXT': {
        'NEW_USER': 'Добро пожаловать в режим тренировки слов и выражений на немецком языке.'
                    ' Здесь я помогу вам потренировать и запомнить слова, которые вы хотели бы выучить.'
                    ' Но прежде, вам необходимо продиктовать слова или фразы и их значения, чтобы я создала список,'
                    ' по которому буду вас тренировать.',
        'OLD_USER': 'Рада снова вас видеть. Давайте продолжим изучать немецкие слова и выражения.'
                    ' Хотите выбрать существующий список или создать новый?'
    },
    'START': 'Команда для начала тренинга: "Начни тренинг".'
             ' Перед стартом можно выбрать список: "Выбери список"'
             ' + <имя списка> Если список не выбран, будет выбран случайный список.',
    'NEW': 'Команда для добавления списка: Создай новый список + <имя списка>.',
    'SHOW': 'По команде "Покажи мои списки" покажу ваши списки.',
    'CREATE_LIST': 'Введите список слов, (словосочетаний) в формате немецкое слово разделитель перевод.'
                   ' В качестве разделителя используйте двоеточие или дефис, в качестве разделителя элементов (строк)'
                   ' списка - символ перевода строки. Строки длиннее 64 символов будут отброшены',
    'END_LIST': 'Поздравляю, вы выучили весь список слов и выражений! sil <[500]>'
                ' Хотите потренировать слова из других списков?'
}

titles = {
    'START': 'Начать тренинг',
    'NEW': 'Создать список',
    'SHOW': 'Показать списки',
}

MODE = {
    'NEW_USER': ['NEW'],
    'OLD_USER': ['START', 'NEW', 'SHOW']
}

ALFABET = 'ÄäÖöÜüß'

"""
    Вопросы
"""
SPEAKER = 'speaker audio="dialogs-upload'
EXCELLENT = '874c6dcf-c804-4d1a-aa5f-e80ac9aad43c'
FAIL = '6fa4bf54-54e3-4b18-9f41-352112d51b42'
SIL = 700
