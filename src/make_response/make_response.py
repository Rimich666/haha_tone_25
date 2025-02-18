import resources
from responses.created_list_responses import confirm_select_new, refuse_select_new, unknown_select_new
from responses.end_list_response import next_list, again, end_learn, unknown_end_list
from responses.first_page_response import insert_list, show_lists, not_command, req_list_name, start_help, what_can
from responses.hint_response import understand_hint, next_synonym, skip_word, spell, synonym
from responses.initialize_response import get_start_message, initialize
from responses.list_name_response import auto_name, confirm_name, refuse_name, query_list_name
from responses.make_list_responses import make_list
from responses.select_list_name_response import select_list, confirm_select_name, refuse_select_name, on_tell_name

from responses.select_list_responses import begin_again, resume, whatever
from responses.question_response import check_answer, stop_training
from helpers.helpers import get_command, get_slots, reset, rebase
from responses.close_response import get_close_response
from responses.training_responses import start_training, not_understand_training
from setings.state import State


def make_response(intents, state, payload, session, tokens, original):
    command = get_command(payload, intents)
    print(command)
    if command == 'RESET':
        return reset()

    if command == 'REBASE':
        return rebase()

    node = 0 if session.get('new') else state['state']
    user_name = session.get('user').get('user_id')
    rsp = {'text': '', 'end_session': False}
    user_id = state.get('user', None)
    is_old = not not user_id
    if command == 'CLOSE':
        return get_close_response(user_id)

    slots = get_slots(intents, command)



    def skip_move():
        return get_start_message('Тут ещё ничего не придумано', '', user_id)

    def help_standalone():
        print('help_request_name')
        rsp['text'], rsp['tts'] = resources.sources[state['state']].help(state['state'])
        rsp['tts'] = rsp['tts'] + state.get('tts', '')
        print(rsp['tts'])
        return state, rsp

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
            'HELP': [help_standalone],
        },
        State.CREATE_LIST: {
            'NO_COMMAND': [make_list, state, original, rsp],
            'HELP': [help_standalone],
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
            'SKIP': [skip_word, state, rsp],
            'STOP': [stop_training, user_id],
            'HELP': [help_standalone],
        },
        State.END_LIST: {
            'NO_COMMAND': [unknown_end_list, state, original],
            'NO': [end_learn, state],
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
            'HELP': [help_standalone],
            'STOP': [stop_training, user_id]
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
