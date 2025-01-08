DICT_API_KEY = 'dict.1.1.20241230T092206Z.ba9a5db11c2aadec.8888be2957feb67ffbe9ab39f37a7812c9de1615'
DICT_URL = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup'

check_images = {
        True: '1030494/aeaac6f5e4866ee83eaf',
        False: '1540737/3767a411c46814372595'
    }

mode_images = {
    'NEW': '1540737/a0df801b838190067c9d',
    'START': '965417/307b56a1df136b4784bb',
    'SHOW': '937455/1ef159a26459009bdeb0'
}

descriptions = {
    'START_TEXT': 'Добро пожаловать в режим тренировки слов и выражений на немецком языке.'
                  ' Здесь я помогу вам потренировать и запомнить слова, которые вы хотели бы выучить.'
                  ' Но прежде, вам необходимо продиктовать слова или фразы и их значения, чтобы я создала список,'
                  ' по которому буду вас тренировать.',
    'START': 'Команда для начала тренинга: "Начни тренинг".'
             ' Перед стартом можно выбрать список: "Выбери список"'
             ' + <имя списка> Если список не выбран, будет выбран случайный список.',
    'NEW': 'Команда для добавления списка: Создай новый список + <имя списка>.',
    'SHOW': 'По команде "Покажи мои списки" покажу ваши списки.',
    'CREATE_LIST': 'Введите список слов (словосочетаний) в формате немецкое слово разделитель перевод.'
                   ' В качестве разделителя используйте двоеточие или дефис, в качестве разделителя элементов (строк)'
                   ' списка - символ перевода строки. Строки длиннее 64 символов будут отброшены'
}

titles = {
    'START': 'Начать тренинг',
    'NEW': 'Создать список',
    'SHOW': 'Показать списки',
}

mode = ['START', 'NEW', 'SHOW']



ALFABET = 'ÄäÖöÜüß'