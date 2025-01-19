from helpers import create_list_name
from responses.a_initialize import get_start_message
from resources import first
from setings.state import State


def insert_list(slots, user_name, state, rsp):
    if not slots:
        return req_list_name(state, rsp)
    name, id = create_list_name(user_name, '' if not slots else slots['what']['value'])
    state['state'] = State.CREATE_LIST
    state['name'] = name
    state['user'] = id
    rsp['text'] = first.create_list.text(name)
    rsp['tts'] = first.create_list.tts(name)
    return state, rsp


def show_lists(state, rsp):
    return state, rsp


def not_command(is_old, original, user_id):
    texts = first.no_command(is_old)
    state, rsp = get_start_message(
        texts.text(original),
        texts.tts(original),
        user_id
    )
    print(state, rsp)
    return state, rsp


def req_list_name(state, rsp):
    attempt = state.get('attempt', 0)
    state['attempt'] = attempt + 1
    state['state'] = State.REQUEST_NAME
    rsp['text'] = first.quest_list_name.text()
    return state, rsp
