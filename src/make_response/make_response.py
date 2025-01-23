import resources
from responses.end_list_response import next_list, again
from responses.first_page import not_command, insert_list, req_list_name, show_lists, what_can, start_help
from responses.hint_response import understand_hint, next_synonym, skip_word, spell, synonym
from responses.list_name import query_list_name, auto_name, confirm_name, refuse_name, help_request_name
from responses.select_list import begin_again, resume, whatever
from responses.select_list_name import select_list, confirm_select_name, refuse_select_name, on_tell_name
from responses.training import start_training, not_understand_training
from responses.question_response import check_answer
from helpers.helpers import get_command, get_slots, get_close_response, reset, rebase
from responses.make_list import make_list
from responses.a_initialize import initialize, get_start_message
from responses.u_created_list import confirm_select_new, refuse_select_new, unknown_select_new
from setings.state import State


def make_response(intents, state, payload, session, tokens, original):
    command = get_command(payload, intents)
    if command == 'CLOSE':
        return get_close_response()

    if command == 'RESET':
        return reset()

    if command == 'REBASE':
        return rebase()

    node = 0 if session.get('new') else state['state']
    user_name = session.get('user').get('user_id')
    rsp = {'text': '', 'end_session': False}
    user_id = state.get('user', None)
    is_old = not not user_id
    slots = get_slots(intents, command)

    def skip_move():
        return get_start_message('Тут ещё ничего не придумано', '', user_id)

    switch_state = {
        State.INIT: {
            'NO_COMMAND': [initialize, user_name]
        },
        State.START: {
            'NEW': [insert_list, slots, user_name, state, rsp],
            'SHOW': [show_lists, state, rsp],
            'SELECT_LIST': [select_list, user_name, slots, state, rsp],
            'NO_COMMAND': [not_command, is_old, original, user_id],
            'YES': [req_list_name, state, rsp],
            'HELP': [start_help, state],
            'WHAT_CAN': [what_can, state]
        },
        State.REQUEST_NAME: {
            'AUTO': [auto_name, state, rsp, user_name],
            'NO_COMMAND': [query_list_name, state, tokens, rsp],
            'YES': [confirm_name, state, rsp, user_name],
            'NO': [refuse_name, state, rsp],
            'HELP': [help_request_name, state, rsp],
        },
        State.CREATE_LIST: {
            'NO_COMMAND': [make_list, state, original, rsp],
            'HELP': [skip_move],
        },
        State.SELECT_LIST: {
            'AGAIN': [begin_again, state, rsp],
            'RESUME': [resume, state, rsp],
            'NO_COMMAND': [whatever, original, state, rsp],
        },
        State.IS_READY: {
            'YES': [start_training, state, rsp],
            'NO': [skip_move],
            'START': [start_training, state, rsp],
            'NO_COMMAND': [not_understand_training, state, rsp, original],
        },
        State.QUESTION: {
            'NO_COMMAND': [check_answer, state, rsp, tokens],
            'SKIP': [skip_move],
            'STOP': [skip_move]
        },
        State.END_LIST: {
            'NO_COMMAND': [skip_move],
            'NO': [skip_move],
            'FIX': [again, state, rsp],
            'ANOTHER': [next_list, state, rsp],
        },
        State.CREATED_LIST: {
            'YES': [confirm_select_new, state, user_name, rsp],
            'NO': [refuse_select_new, state, rsp],
            'NO_COMMAND': [unknown_select_new, state, rsp],
        },
        State.NAME_SELECT: {
            'YES': [confirm_select_name, user_name, state, rsp],
            'NO': [refuse_select_name, state, rsp],
            'NO_COMMAND': [on_tell_name, original, user_name, state, rsp],
        },
        State.HINT: {
            'NO_COMMAND': [understand_hint, state, rsp],
            'NEXT': [next_synonym, state, rsp],
            'SKIP': [skip_word, state, rsp],
            'SPELL': [spell, state, rsp],
            'SYNONYM': [synonym, state, rsp],
            'HELP': [skip_move],
            'STOP': [skip_move]
        }
    }

    print('make_response', state)
    print('make_response', command, node)
    need_func = switch_state[node][resources.sources[node].check_command(command, is_old if node < 2 else None)]
    func = need_func[0]
    args = need_func[1:]
    state, rsp = func(*args)

    return {
        "version": '1.0',
        "response": rsp,
        "session_state": state
    }
