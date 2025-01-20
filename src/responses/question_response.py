import json

from repository import base
from resources import sources
from responses.training import next_word
from setings.state import State

STATE = State.QUESTION


def select_hint(state, rsp):
    state['state'] = State.HINT
    rsp['text'], rsp['tts'] = sources[STATE].select_hint()
    return state, rsp


def parse_state(state):
    index = state['index']
    words = json.loads(state['words'])
    ids = json.loads(state['ids'])
    right = words[str(ids[index])]['ru'].split(' ')

    return index, words, ids, right


def check_answer(state, rsp, answer):
    index, words, ids, right = parse_state(state)
    is_subset = set(right).issubset(answer)
    if is_subset:
        id = ids.pop(index)
        base.set_is_learn(id)

    return next_word(state, rsp, words, ids, True) if is_subset else select_hint(state, rsp)

