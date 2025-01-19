import random

from repository import base
from resources import name_select
from responses.a_initialize import get_start_message
from responses.select_list import upload_list
from setings.state import State


def query_select_name(state, rsp):
    state['state'] = State.NAME_SELECT
    state['quest'] = True
    rsp['text'] = name_select.list_select.text()
    rsp['tts'] = name_select.list_select.tts()
    print(state)
    print(rsp)
    return state, rsp


def next_name(state, rsp):
    print(state)
    index = state.get('index', -1)
    lists = state['lists']
    index += 1
    if index == len(lists):
        return get_start_message(
            name_select.end_names.text(),
            name_select.end_names.tts(),
            state['user']
        )
    offers = name_select.offers
    offer = offers[random.randrange(len(offers))]
    pref = name_select.no_list
    name = lists[index]
    rsp['text'] = (pref.text(state['name']) if index == 0 else '') + offer.text(name)
    rsp['tts'] = (pref.tts(state['name']) if index == 0 else '') + offer.tts(name)
    state['index'] = index
    state['name'] = name

    return state, rsp


def lists_list(user, state, rsp):
    lists, user_id = base.select_lists(user)
    if len(lists) == 0:
        return get_start_message(
            name_select.no_lists.text(),
            name_select.no_lists.tts(),
            state['user']
        )
    state['quest'] = False
    state['state'] = State.NAME_SELECT
    state['lists'] = [n['name'] for n in lists]
    return next_name(state, rsp)


def on_tell_name(original, user, state, rsp):
    is_quest = state.get('quest', False)
    print(is_quest)
    if not state.get('quest', False):
        rsp['text'] = name_select.dont_understand.text(original)
        rsp['tts'] = name_select.dont_understand.tts(original)
        return state, rsp
    name = original
    list_id, is_loaded = base.get_list_id(user, name)
    state['name'] = name
    if not list_id:
        return lists_list(user, state, rsp)
    return upload_list(user, name)


def confirm_select_name(user, state):
    state.pop('index', None)
    state.pop('quest', None)
    state.pop('lists', None)
    name = state['name']
    return upload_list(user, name)


def refuse_select_name(state, rsp):
    return next_name(state, rsp)


def select_list(user, slots, state, rsp):
    print('select_list', rsp, slots)
    if not slots:
        return query_select_name(state, rsp)
    name = slots['what']['value']
    state['name'] = name
    list_id, is_loaded = base.get_list_id(user, name)
    return upload_list(user, name) if list_id else lists_list(user, state, rsp)
