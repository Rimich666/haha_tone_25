import random

from repository import base
from repository.object_store import ObjectStore
from setings.alfabet import Alfabet
from silero.silero import silero


def create_list_name(user, name):
    lists, user_id = base.select_lists(user)
    names = [i.name for i in lists]
    if name == '' or name in names:
        free_names = base.select_free_names(names)
        return free_names[random.randrange(len(free_names))], user_id
    return name, user_id


def save_list(state, original, rsp, user=1):
    alfabet = Alfabet()
    store = ObjectStore()

    def edit_row(row):
        word_list = list(filter(lambda item: item != '', alfabet.trans(row).lower().split(' ')))
        return [' '.join(filter(lambda wrd: alfabet.check(wrd, lang), word_list)) for lang in [Alfabet.de, Alfabet.ru]]

    words = list(map(lambda item: edit_row(item), filter(lambda item: len(item) < 65, original.split('\n'))))
    new_words = base.select_new_words(words)
    for word in new_words:
        file_name = word[2]
        if not file_name:
            audio = silero(word[0])
            file_name = f'{word[0].replace(' ', '_')}.wav'
            store.upload_string(file_name, audio)

        base.insert_word(word[1], word[0], file_name)

    all_words = base.create_list(words, state['user'], state['name'])
    print(user, state['name'], not not all_words)
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
    result = save_list(fake_state, original_utterance2, fake_rsp)
