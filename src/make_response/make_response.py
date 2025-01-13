from responses.first_page import not_command
from responses.select_list import upload_list, check_load_list
from responses.training import send_word
from .helpers import get_command
from .make_list import save_list, create_list_name
from responses.initialize import initialize
from setings.setings import *
from setings.state import State


def make_response(intents, state, payload, session, request):
    print(session)
    is_new = session.get('new')
    user_id = session.get('user').get('user_id')
    original = request['original_utterance']
    rsp = {'text': '', 'end_session': False}

    def select_list():
        slots = intents['SELECT_LIST']['slots']
        ret_state = {'state': State.SELECT_LIST}
        if not slots:
            return ret_state, {'text': 'Не расслышала имя списка.'}
        ret_state, resp = upload_list(user_id, slots['what']['value'])
        return ret_state, resp

    def show_lists():
        return state, rsp

    def state_start():
        def insert_list():
            slots = intents['NEW']['slots']
            name, id = create_list_name(user_id, '' if not slots else slots['what']['value'])
            return {'state': State.CREATE_LIST, 'name': name, 'user': id}, {'text': first_page_text['CREATE_LIST']}

        def start_training():
            return state, rsp

        def no_command():
            return not_command(user_id, original)

        switch_mode = {
            'START': start_training,
            'NEW': insert_list,
            'SHOW': show_lists,
            'SELECT_LIST': select_list,
            'NO_COMMAND': no_command
        }

        return switch_mode[command]()

    def make_new_list():
        resp = save_list(state, original, rsp, user_id)
        return state, resp

    def selection_list():
        return check_load_list(state)

    def list_is_ready():
        def start_training():
            return send_word(state, rsp)

        switch_mode = {
            'START': start_training,
            'SHOW': show_lists,
            'SELECT_LIST': select_list
        }

        if not intents:
            return state, rsp

        return switch_mode[list(intents.keys())[0]]()

    def question():
        send_word(state, rsp, request['nlu']['tokens'])
        return state, rsp

    def end_list():
        return state, rsp

    command = get_command(payload, intents)
    if command == 'CLOSE':
        return {
            "version": '1.0',
            "response": {'text': '', 'end_session': True}
        }

    switch_state = [state_start, make_new_list, selection_list, list_is_ready, question, end_list()]
    if is_new:
        state, rsp = initialize(user_id)
    else:
        state, rsp = switch_state[state['state']]()

    return {
        "version": '1.0',
        "response": rsp,
        "session_state": state
    }
