import requests

from setings.setings import check_images, DICT_URL, DICT_API_KEY


def get_word_list(tr):
    return [{'text': item['text'], 'check': False } for item in tr[:5]]


def get_items(words):
    return [
                {
                    "image_id": check_images[word['check']],
                    "title": word['text'],
                    "description": f'Для установки или отмены выбора назовите индекс: {index}, или просто кликните',
                    "button": {
                        'payload': {'index': index},
                        "text": "Кнопка",
                    }
                } for index, word in enumerate(words)
           ]


def set_check(check_list, words):
    for index in filter(lambda i: i < len(words), check_list):
        words[index]['check'] = not words[index]['check']
    return words


def new_word(intents, state, rsp):
    value = intents.get("NEW").get("slots").get("what").get("value")
    response = requests.post(DICT_URL, data={'key': DICT_API_KEY, 'lang': 'ru-de', 'text': value})
    definition = response.json().get('def')
    rsp['text'] = f'Добавляю новое слово {value}' if definition else f'Не удалось найти перевод слова {value}'
    if definition:
        words = get_word_list(definition[0].get('tr'))
        state = {
            'state': State.SELECT_WORDS,
            'words': words,
            'value': value
        }

        rsp['card'] = {
            "type": "ItemsList",
            "header": {
                "text": f'Варианты перевода для слова "{value}"',
            },
            "items": get_items(words),
        }
    return state, rsp


def select_word(state, rsp, index):
    rsp['card'] = {
        "type": "ItemsList",
        "header": {
            "text": f'Варианты перевода для слова "{state["value"]}"',
        },
        "items": get_items(set_check(index, state['words'])),
    }
    return state, rsp