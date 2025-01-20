from resources import list_name_res, first
from responses.a_initialize import get_start_message
from responses.first_page import insert_list, req_list_name


def query_list_name(state, tokens, rsp):
    name = ' '.join(tokens[:2])
    state['name'] = name
    rsp['text'] = list_name_res.check.text(name)
    return state, rsp


def auto_name(state, rsp, user_name):
    return insert_list(None, user_name, state, rsp)


def confirm_name(state, rsp, user_name):
    name = state.get('name', '')
    attempt = state.pop('attempt', None)

    return insert_list(
        None if attempt == len(list_name_res.extents) else {'what': {'value': name}}, user_name, state, rsp)


def refuse_name(state, rsp):
    ext = list_name_res.extents
    len_ext = len(ext)
    attempt = state['attempt']
    if (attempt - 1) == len_ext:
        is_old = not not state['user']
        text, tts = first.get_no_command(is_old)
        state, rsp = get_start_message(text, tts, state['user'])
        return state, rsp
    state, rsp = req_list_name(state, rsp)
    state['name'] = ''

    text = ext[attempt - 1].text()
    tts = ext[attempt - 1].tts()
    if text:
        rsp['text'] = text
    rsp['tts'] = tts
    return state, rsp
