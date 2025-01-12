from responses.select_list import upload_list, check_load_list
from responses.training import send_word
from .make_list import save_list, create_list_name
from responses.initialize import initialize
from setings.setings import *
from setings.state import State


def make_response(intents, state, payload, session, request):
    print(session)
    is_new = session.get('new')
    user_id = session.get('user').get('user_id')
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
            return {'state': State.CREATE_LIST, 'name': name, 'user': id}, {'text': descriptions['CREATE_LIST']}

        def start_training():
            return state, rsp

        switch_mode = {
            'START': start_training,
            'NEW': insert_list,
            'SHOW': show_lists,
            'SELECT_LIST': select_list
        }

        if not payload and not intents:
            return state, rsp
        return switch_mode[payload['mode'] if payload else list(intents.keys())[0]]()

    def make_new_list():
        resp = save_list(state, request['original_utterance'], rsp, user_id)
        return state, resp

    def selection_list():
        return check_load_list(state)

    def list_is_ready():
        def start_training():
            return send_word(state, rsp)
            # return state, rsp

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

    switch_state = [state_start, make_new_list, selection_list, list_is_ready, question, end_list()]
    if is_new:
        state, rsp = initialize()
    else:
        state, rsp = switch_state[state['state']]()

    # elif state['state'] == state.START:
    #     print(state)
    # elif 'NEW' in intents:
    #     state, rsp = new_word(intents, state, rsp)
    # elif state['state'] == State.SELECT_WORDS:
    #     if payload:
    #         state, rsp = select_word(state, rsp, [payload['index']])
    #     elif request['nlu']['entities']:
    #         state, rsp = select_word(state, rsp, list(map(lambda i: int(i['value']),
    #                     filter(lambda i: i['type'] == 'YANDEX.NUMBER', request['nlu']['entities']))))
    #     elif 'SAVE' in intents:
    #         print('save')
    #         print(base)
    print(rsp)
    return {
        "version": '1.0',
        "response": rsp,
        "session_state": state
    }
