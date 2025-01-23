from helpers.helpers import parse_state
from repository import base
from resources import sources
from responses.initialize_response import get_start_message
from responses.select_list_name import query_select_name
from responses.training_responses import next_word
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


def end_learn(state):
    text, tts = sources[STATE].back()
    return get_start_message(text, tts, state['user'])


def unknown_end_list(state, original):
    text, tts = sources[STATE].not_understand(original)
    return get_start_message(text, tts, state['user'])

