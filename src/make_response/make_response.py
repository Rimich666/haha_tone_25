import resources
from responses import select_list
from responses.first_page import not_command, insert_list, req_list_name, show_lists
from responses.list_name import query_list_name, auto_name, confirm_name, refuse_name
from responses.select_list import check_load_list
from responses.training import send_word
from helpers import get_command, get_slots, get_close_response, reset
from responses.make_list import make_list
from responses.a_initialize import initialize


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
        return state, rsp

    switch_state = [
        {
            'NO_COMMAND': [initialize, user_name]
        },
        {
            'START': [skip_move],
            'NEW': [insert_list, slots, user_name, state, rsp],
            'SHOW': [show_lists, state, rsp],
            'SELECT_LIST': [select_list, slots, user_name],
            'NO_COMMAND': [not_command, is_old, original],
            'YES': [req_list_name, state, rsp],
        },
        {
            'AUTO': [auto_name, state, rsp, user_name],
            'NO_COMMAND': [query_list_name, state, tokens, rsp],
            'YES': [confirm_name, state, rsp, user_name],
            'NO': [refuse_name, state, rsp]
        },
        {
            'NO_COMMAND': [make_list, state, original, rsp, user_name],
        },
        {
            'NO_COMMAND': [check_load_list, state, rsp],
        },
        {
            'START': [send_word, state, rsp],
            'SHOW': [show_lists],
            'SELECT_LIST': [select_list],
            'NO_COMMAND': [skip_move],
        },
        {
            'NO_COMMAND': [send_word, state, rsp, tokens],
        },
        {
            'NO_COMMAND': [skip_move],
        }]

    print(resources.sources, node)
    need_func = switch_state[node][resources.sources[node].check_command(command, is_old if node < 2 else None)]
    func = need_func[0]
    args = need_func[1:]
    state, rsp = func(*args)

    return {
        "version": '1.0',
        "response": rsp,
        "session_state": state
    }
