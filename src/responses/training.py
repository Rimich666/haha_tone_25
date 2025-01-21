import json
import random
from repository import base
from resources import sources
from setings.state import State

STATE = State.IS_READY


def query_words(list_id):
    print('querying words...')
    _, is_loaded = base.get_list_is_loaded(list_id)
    print(is_loaded)
    words = {
        str(w['id']):
            {
                'ru': w['ru'],
                'de': w['de'],
                'audio_id': w['audio_id'],
                'learned': w['learned']
            } for w in base.select_words_list(list_id, True)}

    print(words)

    index = list(item[0] for item in words.items() if not item[1]['learned'] or not is_loaded)

    return words, index, is_loaded


def end_list(state, rsp):
    state.pop('index', None)
    state['state'] = State.END_LIST
    rsp['text'], rsp['tts'] = sources[STATE].end_list()
    return state, rsp


def next_word(state, rsp, words=None, ids=None, is_excellent=None):
    if not state['loaded']:
        words, ids, is_loaded = query_words(state['list_id'])
        state['words'] = json.dumps(words)
        state['loaded'] = is_loaded
    count = len(ids)
    if count == 0:
        return end_list(state, rsp)
    index = 0 if count == 1 else random.randrange(count)
    word = words[str(ids[index])]
    state['index'] = index
    state['state'] = State.QUESTION
    state['ids'] = json.dumps(ids)

    rsp['text'], rsp['tts'] = sources[STATE].question(word, is_excellent)
    return state, rsp


def start_training(state, rsp):
    state['loaded'] = False
    state, rsp = next_word(state, rsp)
    rsp['tts'] = sources[STATE].start() + rsp['tts']
    return state, rsp


def not_understand_training(state, rsp, original):
    rsp['text'], rsp['tts'] = sources[STATE].dont_understand(original)
    return state, rsp


def cancel_training(state, rsp):
    return state, rsp
