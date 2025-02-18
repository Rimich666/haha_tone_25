import threading

from load_resource.load_audio import LoadAudio
from repository.object_store import ObjectStore
from repository.queries import get_words_by_id, create_list, insert_new_words, set_created_list, set_audio_id, \
    select_without_file, insert_audio, get_file_path
from resources import sources
from setings.alfabet import Alfabet
from setings.state import State
from silero.silero import silero


STATE = State.CREATE_LIST


def save_list(*args):
    store = ObjectStore()
    loader = LoadAudio()
    words, list_id, is_head = args

    def create_word(word):
        record = get_file_path(word)
        if record:
            return record[0]['file_path']
        audio = silero(word)
        file_name = f'{word.replace(' ', '_')}.wav'
        store.upload_string(file_name, audio)
        insert_audio(word, file_name)
        return file_name

    out_files = words if select_without_file(words) else words
    for i, w in enumerate(out_files):
        file_path = create_word(w['de'])
        if i < 3:
            audio_id = loader.load_file(file_path)
            set_audio_id(w['id'], list_id, audio_id)

    set_created_list(list_id)


def bad_list(state, rsp):
    rsp['text'], rsp['tts'] = sources[STATE].bad_list()
    return state, rsp


def make_list(state, original, rsp):
    alfabet = Alfabet()

    def edit_row(row):
        word_list = list(filter(lambda item: item != '', alfabet.trans(row).lower().split(' ')))
        word = [' '.join(filter(lambda wrd: alfabet.check(wrd, lang), word_list)) for lang in [Alfabet.de, Alfabet.ru]]
        if len(word) != 2:
            return []
        if len(word[0]) * len(word[1]) == 0:
            return []
        return [' '.join(filter(lambda wrd: alfabet.check(wrd, lang), word_list)) for lang in [Alfabet.de, Alfabet.ru]]

    words = list(filter(lambda word: not not word, map(
        lambda item: edit_row(item), filter(lambda item: len(item) < 65, original.split('\n')))))[:20]
    if not words:
        return bad_list(state, rsp)
    new_words = insert_new_words(words).rows
    new_count = len(new_words)
    choice = new_count // 6
    is_head = not new_words
    list_id, head_id = create_list(words, state['user'], state['name'], len(words))
    head = get_words_by_id([str(rec['word_id']) for rec in head_id]) if is_head else []
    thread = threading.Thread(target=save_list, args=(head if is_head else new_words, list_id, is_head))
    thread.start()

    state['list_id'] = list_id
    return created_response(state, rsp)


def created_response(state, rsp):
    state['state'] = State.CREATED_LIST
    rsp['text'], rsp['tts'] = sources[STATE].list_created(state['name'])
    state['tts'] = rsp['tts']
    return state, rsp


def wait_create_response(state, rsp):
    state['state'] = State.WAIT_CREATE_LIST
    rsp['text'], rsp['tts'] = sources[STATE].list_create_wait(state['name'])
    return state, rsp
