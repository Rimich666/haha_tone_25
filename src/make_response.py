import requests
from src.setings import *
from src.state import State
from src.word_list import *
from repository.repository import base


def initialize():
    return {'state': State.START}, {'text': START_DESCRIPTION, 'end_session': False}


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


def make_response(intents, state, payload, is_new, request):
    rsp = {'text': '', 'end_session': False}
    if is_new:
        state, rsp = initialize()
    elif 'NEW' in intents:
        state, rsp = new_word(intents, state, rsp)
    elif state['state'] == State.SELECT_WORDS:
        if payload:
            state, rsp = select_word(state, rsp, [payload['index']])
        elif request['nlu']['entities']:
            state, rsp = select_word(state, rsp, list(map(lambda i: int(i['value']),
                        filter(lambda i: i['type'] == 'YANDEX.NUMBER', request['nlu']['entities']))))
        elif 'SAVE' in intents:
            print('save')
            print(base)
    return {
        "version": '1.0',
        "response": rsp,
        "session_state": state
    }
