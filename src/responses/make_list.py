import threading

from load_resource.load_audio import LoadAudio
from repository import base
from repository.object_store import ObjectStore
from resources import create_list, sources
from setings.alfabet import Alfabet
from setings.state import State
from silero.silero import silero


STATE = State.CREATE_LIST


def save_list(*args):
    store = ObjectStore()
    loader = LoadAudio()
    words, list_id, is_head = args

    def create_word(word):
        record = base.get_file_path(word)
        if record:
            return record[0]['file_path']
        audio = silero(word)
        file_name = f'{word.replace(' ', '_')}.wav'
        store.upload_string(file_name, audio)
        base.insert_audio(word, file_name)
        return file_name

    out_files = words if base.select_without_file(words) else words
    for i, w in enumerate(out_files):
        file_path = create_word(w['de'])
        if i < 3:
            audio_id = loader.load_file(file_path)
            base.set_audio_id(w['id'], list_id, audio_id)
    base.set_created_list(list_id)


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
        lambda item: edit_row(item), filter(lambda item: len(item) < 65, original.split('\n')))))
    if not words:
        return bad_list(state, rsp)
    new_words = base.insert_new_words(words).rows
    is_head = not new_words
    list_id, head_id = base.create_list(words, state['user'], state['name'], len(words))
    head = base.get_words_by_id([str(rec['word_id']) for rec in head_id]) if is_head else []
    thread = threading.Thread(target=save_list, args=(head if is_head else new_words, list_id, is_head))
    thread.start()

    state['state'] = State.CREATED_LIST
    state['list_id'] = list_id
    rsp['text'] = sources[STATE].list_created.text(state['name'])
    rsp['tts'] = sources[STATE].list_created.tts(state['name'])
    return state, rsp


if __name__ == '__main__':
    original_utterance = '''das Buch - книга
das Fahrrad - велосипед
das Fieber - жар, (высокая) температура
der Nachmittag - время после полудня
der Arzt - врач
der Geburtsort - место рождения
wie - как
der November - ноябрь
die Wassermelone - арбуз
das Verb - глаголы
der Pfad - тропа, тропинка
der Nachmittag - время до полудня
das Gemüse — овощи
jeder - каждый
die Serviette - салфетка
das Kind - ребенок
der Stock - палка
die Konsequenz - (по)следствие'''

    original_utterance1 = '''das Buch - супер книга
        der November - ноябрь
        die Wassermelone - супер арбуз
        das Verb - глаголы
        der Pfad - тропа, тропинка
        der Nachmittag - время до полудня
        das Gemüse — супер овощи
        die Gans - гусь
        die Tante - тетя
        das Büro - офис
        der Stock - палка
        die Konsequenz - (по)следствие'''
    original_utterance2 = '''das Buch - книга
    das Fahrrad - велосипед
    das Fieber - жар, (высокая) температура
    der Nachmittag - время после полудня
    der Arzt - врач
    der Geburtsort - место рождения
    🇩🇪die Familie - семья
    der Enkel - внук
    das Zimmer - комната
    letzt - последний, прошлый
    der Urlaub - отпуск
    die Zucchini [цукини] - кабачок
    die Gans - гусь
    die Tante - тетя
    das Büro - офис
    die Fäustlinge - варежки
    die Kusine - двоюродная сестра
    die Tafel - доска (школьная)
    die Brücke - мост
    senden - посылать
    der Hund - собака
    das Treffen - встреча
    das Sakko - пиджак
    wie - как
    der November - ноябрь
    die Wassermelone - арбуз
    das Verb - глаголы
    der Pfad - тропа, тропинка
    der Nachmittag - время до полудня
    das Gemüse — овощи
    jeder - каждый
    die Serviette - салфетка
    das Kind - ребенок
    der Stock - палка
    die Konsequenz - (по)следствие'''
    fake_state = {'state': 1}
    fake_rsp = {'text': '', 'end_session': False}
    res = make_list(fake_state, original_utterance, fake_rsp)
