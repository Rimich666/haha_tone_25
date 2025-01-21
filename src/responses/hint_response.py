import json

from helpers.first_syllable import extract_first_syllable
from helpers.helpers import parse_state
from helpers.synonyms import get_synonyms
from resources import sources
from responses.training import next_word
from setings.state import State

STATE = State.HINT


def skip_word(state, rsp):
    print('skip word', state)
    _, words, ids = parse_state(state)
    next_word(state, rsp, words, ids)
    return state, rsp


def understand_hint(state, rsp):
    print('understand hint', state)
    return state, rsp


def next_synonym(state, rsp):
    print('next synonym', state)
    return state, rsp


def spell(state, rsp):
    print('spell', state)
    index, words, ids = parse_state(state)
    word = words[str(ids[index])]
    spell = extract_first_syllable(word['ru'].split(' '))
    rsp['text'], rsp['tts'] = sources[STATE].spell(spell)
    state['state'] = State.QUESTION
    return state, rsp


def synonym(state, rsp):
    index, words, ids = parse_state(state)
    word = words[str(ids[index])]['ru']
    synonyms = get_synonyms(word)
    state['state'] = State.QUESTION
    if synonyms:
        rsp['text'], rsp['tts'] = sources[STATE].synonym(synonyms[0])
        state['synonyms'] = json.dumps(synonyms)
        state['synonym'] = 0
        return state, rsp
    return state, rsp
