from helpers.helpers import create_list_name
from resources import first, sources
from responses.initialize_response import get_start_message
from setings.state import State

STATE = State.START


def insert_list(slots, user_name, state, rsp):
    if not slots:
        return req_list_name(state, rsp)
    name, id = create_list_name(user_name, '' if not slots else slots['what']['value'])
    state['state'] = State.CREATE_LIST
    state['name'] = name
    state['user'] = id
    rsp['text'] = first.create_list.text(name)
    rsp['tts'] = first.create_list.tts(name)
    state['tts'] = rsp['tts']
    return state, rsp


def show_lists(state, rsp):
    return state, rsp


def start_help(state):
    text, tts = sources[STATE].get_help()
    user = state.get('user', None)
    return get_start_message(text, tts, user)


def what_can(state):
    text, tts = sources[STATE].get_wat_can()
    user = state.get('user', None)
    return get_start_message(text, tts, user)


def not_command(is_old, original, user_id):
    texts = first.no_command(is_old)
    state, rsp = get_start_message(
        texts.text(original),
        texts.tts(original),
        user_id
    )
    return state, rsp


def req_list_name(state, rsp):
    attempt = state.get('attempt', 0)
    state['attempt'] = attempt + 1
    state['state'] = State.REQUEST_NAME
    state['tts'] = rsp['text'] = first.quest_list_name.text()

    return state, rsp
