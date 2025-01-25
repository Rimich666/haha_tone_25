from helpers.helpers import parse_state
from repository.queries import set_is_learn
from resources import sources
from responses.initialize_response import get_start_message
from responses.training_responses import next_word
from setings.state import State

STATE = State.QUESTION


def select_hint(state, rsp):
    state['state'] = State.HINT
    rsp['text'], rsp['tts'] = sources[STATE].select_hint()
    return state, rsp


def check_answer(state, rsp, answer):
    index, words, ids = parse_state(state)
    right = words[str(ids[index])]['ru'].split(' ')
    is_subset = set(right).issubset(answer)
    if is_subset:
        id = ids.pop(index)
        set_is_learn(id)

    return next_word(state, rsp, words, ids, True) if is_subset else select_hint(state, rsp)


def stop_training(user):
    text, tts = sources[STATE].stop()
    return get_start_message(text, tts, user)