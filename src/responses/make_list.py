import threading

from load_resource.load_audio import LoadAudio
from repository import base
from repository.object_store import ObjectStore
from resources import create_list
from setings.alfabet import Alfabet
from setings.state import State
from silero.silero import silero


def save_list(*args):
    store = ObjectStore()
    loader = LoadAudio()

    def create_word(word):
        record = base.get_file_path(word).rows
        if record:
            return record[0]['file_path']
        audio = silero(word)
        file_name = f'{word.replace(' ', '_')}.wav'
        store.upload_string(file_name, audio)
        base.insert_audio(word, file_name)
        return file_name
    print(args[0])
    out_files = base.select_without_file(args[0])
    for i, w in enumerate(out_files):
        print(w, i)
        file_path = create_word(w['de'])
        if i < 3:
            audio_id = loader.load_file(file_path)
            base.set_audio_id(w['id'], args[1], audio_id)

    # print(new_words)
    # print(out_files)


def make_list(state, original, rsp):
    alfabet = Alfabet()

    def edit_row(row):
        word_list = list(filter(lambda item: item != '', alfabet.trans(row).lower().split(' ')))
        return [' '.join(filter(lambda wrd: alfabet.check(wrd, lang), word_list)) for lang in [Alfabet.de, Alfabet.ru]]

    words = list(map(lambda item: edit_row(item), filter(lambda item: len(item) < 65, original.split('\n'))))
    new_words = base.insert_new_words(words).rows
    print(new_words)
    list_id = base.create_list(words, state['user'], state['name'])
    thread = threading.Thread(target=save_list, args=(new_words, list_id))
    thread.start()

    state['state'] = State.CREATED_LIST
    state['list_id'] = list_id
    rsp['text'] = create_list.list_created.text(state['name'])
    rsp['tts'] = create_list.list_created.tts(state['name'])
    print('make_list', state, rsp)
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
