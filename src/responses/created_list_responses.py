from load_resource.load_audio import LoadAudio
from repository import base
from responses.select_list_responses import upload_list


def check_added(state):
    loder = LoadAudio()
    list_id = state['list_id']
    added_words = base.get_added_words(list_id, True)
    for word in added_words:
        status = loder.get_status(word['audio_id'])
        if status:
            base.set_is_processed(word['id'])


def confirm_select_new(state, user, rsp):
    check_added(state)
    print('confirm_select_new', user, state['name'])
    return upload_list(user, state['name'], state, rsp)


def refuse_select_new(state, rsp):
    print('refuse_select_new')
    check_added(state)
    return state, rsp


def unknown_select_new(state, rsp):
    print('unknown_select_new')
    check_added(state)
    return state, rsp
