import resources
from responses.first_page import not_command, insert_list, req_list_name, show_lists
from responses.list_name import query_list_name, auto_name, confirm_name, refuse_name
# from responses.select_list import check_load_list
from responses.select_list_name import select_list, confirm_select_name, refuse_select_name, on_tell_name
from responses.training import send_word
from helpers import get_command, get_slots, get_close_response, reset
from responses.make_list import make_list
from responses.a_initialize import initialize
from responses.u_created_list import confirm_select_new, refuse_select_new, unknown_select_new
from setings.state import State


def make_response(intents, state, payload, session, tokens, original):
    command = get_command(payload, intents)
    if command == 'CLOSE':
        return get_close_response()

    if command == 'RESET':
        return reset()

    node = 0 if session.get('new') else state['state']
    user_name = session.get('user').get('user_id')
    rsp = {'text': '', 'end_session': False}
    user_id = state.get('user', None)
    is_old = not not user_id
    slots = get_slots(intents, command)

    def skip_move():
        print('skip')
        return state, rsp

    switch_state = {
        State.INIT: {
            'NO_COMMAND': [initialize, user_name]
        },
        State.START: {
            'START': [skip_move],
            'NEW': [insert_list, slots, user_name, state, rsp],
            'SHOW': [show_lists, state, rsp],
            'SELECT_LIST': [select_list, user_name, slots, state, rsp],
            'NO_COMMAND': [not_command, is_old, original, user_id],
            'YES': [req_list_name, state, rsp],
        },
        State.REQUEST_NAME: {
            'AUTO': [auto_name, state, rsp, user_name],
            'NO_COMMAND': [query_list_name, state, tokens, rsp],
            'YES': [confirm_name, state, rsp, user_name],
            'NO': [refuse_name, state, rsp]
        },
        State.CREATE_LIST: {
            'NO_COMMAND': [make_list, state, original, rsp],
        },
        State.SELECT_LIST: {
            'NO_COMMAND': [skip_move],
        },
        State.IS_LOADED: {
            'START': [send_word, state, rsp],
            'SHOW': [show_lists],
            'SELECT_LIST': [select_list],
            'NO_COMMAND': [skip_move],
        },
        State.QUESTION: {
            'NO_COMMAND': [send_word, state, rsp, tokens],
        },
        State.END_LIST: {
            'NO_COMMAND': [skip_move],
        },
        State.CREATED_LIST: {
            'YES': [confirm_select_new, state, user_name],
            'NO': [refuse_select_new, state, rsp],
            'NO_COMMAND': [unknown_select_new, state, rsp],
        },
        State.NAME_SELECT: {
            'YES': [confirm_select_name, user_name, state],
            'NO': [refuse_select_name, state, rsp],
            'NO_COMMAND': [on_tell_name, original, user_name, state, rsp],
        },
    }

    print(state, command)
    need_func = switch_state[node][resources.sources[node].check_command(command, is_old if node < 2 else None)]
    func = need_func[0]
    args = need_func[1:]
    state, rsp = func(*args)
    print(rsp)

    return {
        "version": '1.0',
        "response": rsp,
        "session_state": state
    }
