import asyncio
import json
import threading
import time

from repository import base
from repository.object_store import ObjectStore
from setings.alfabet import Alfabet
from silero.silero import silero


async def save_list(state, original, rsp, user_name):
    alfabet = Alfabet()
    store = ObjectStore()

    async def create_word(word):
        start = time.time()
        file_name = word[2]
        if not file_name:
            audio = silero(word[0])
            file_name = f'{word[0].replace(' ', '_')}.wav'
            store.upload_string(file_name, audio)

        base.insert_word(word[1], word[0], file_name)
        progress = json.loads(store.get_object(user_name))
        store.upload_string(user_name, json.dumps({'all': progress['all'], 'cur': progress['cur'] + 1}))
        return time.time() - start

    def edit_row(row):
        word_list = list(filter(lambda item: item != '', alfabet.trans(row).lower().split(' ')))
        return [' '.join(filter(lambda wrd: alfabet.check(wrd, lang), word_list)) for lang in [Alfabet.de, Alfabet.ru]]

    words = list(map(lambda item: edit_row(item), filter(lambda item: len(item) < 65, original.split('\n'))))
    new_words = base.select_new_words(words)
    store.upload_string(user_name, json.dumps({'all': len(new_words), 'cur': 0}))

    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(create_word(w)) for w in new_words]

    result = sum([t.result() for t in tasks]) / len(tasks)
    print(json.loads(store.get_object(user_name)))
    print('средний тайм =', result)
    store.delete_by_key(user_name)
    all_words = base.create_list(words, state['user'], state['name'])
    print(user_name, ' ', state['name'], not not all_words)
    return state, rsp


def start_creat_thread(state, original, rsp, user_name):
    asyncio.run(save_list(state, original, rsp, user_name))


def make_list(state, original, rsp, user_name):
    thread = threading.Thread(target=start_creat_thread, args=(state, original, rsp, user_name))
    thread.start()
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
