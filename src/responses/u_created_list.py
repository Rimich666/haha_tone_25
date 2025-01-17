from repository import base


def confirm_select_new(state, rsp):
    print('confirm_select_new')
    return state, rsp


def refuse_select_new(state, rsp):
    print('refuse_select_new')
    return state, rsp


def unknown_select_new(state, rsp):
    print('unknown_select_new')
    return state, rsp


func = {
    'YES': confirm_select_new,
    'NO': refuse_select_new,
    'NO_COMMAND': unknown_select_new
}


def select_new(state, rsp, command):
    list_id = state['list_id']
    added_words = base.get_added_words(list_id)
    print('select_new')
    print('state:', state)
    return func[command](state, rsp)
