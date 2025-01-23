from helpers.helpers import parse_state
from repository import base
from responses.select_list_name import query_select_name
from responses.training import next_word
from setings.state import State

STATE = State.END_LIST


def next_list(state, rsp):
    return query_select_name(state, rsp)


def again(state, rsp):
    list_id = state['list_id']
    _, words, _ = parse_state(state)
    ids = list(words.keys())
    base.reset_words_learning(list_id)

    return next_word(state, rsp, words, ids)


def end_learn(state, rsp):
    return state, rsp


def unknown(state, rsp, original):
    return state, rsp

