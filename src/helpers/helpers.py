import json
import random
import threading

from load_resource.load_audio import LoadAudio
from repository.object_store import ObjectStore
from repository.queries import select_lists, select_free_names, select_all_audio, clear_tables, drop_tables, \
    create_tables
from setings.setings import word_case


def get_command(payload, intents):
    if payload:
        mode = payload.get('mode', None)
        if mode:
            return mode
    if intents:
        for i in intents.keys():
            if not i.startswith('YANDEX'):
                return i
    return 'NO_COMMAND'


def get_slots(intents, command):
    if command == 'NO_COMMAND':
        return None
    return intents[command]['slots']


def get_close_response():
    print('get_close_response')
    return {
        "version": '1.0',
        "response": {'text': '', 'end_session': True}
    }


def create_list_name(user, name):
    lists, user_id = select_lists(user)
    names = [i.name for i in lists]
    if name == '' or name in names:
        free_names = select_free_names(names)
        return free_names[random.randrange(len(free_names))], user_id
    return name, user_id


def clear_all():
    print('clear_all')
    store = ObjectStore()
    loder = LoadAudio()
    ids = select_all_audio()
    if ids:
        for id in [i['audio_id']for i in ids]:
            loder.delete(id)
    store.delete()
    clear_tables()


def recreate_all_table():
    print('clear')
    clear_all()
    print('drop')
    drop_tables()
    print('create')
    create_tables()
    print("that's all")


def reset():
    print('Обнуляем данные.')
    thread = threading.Thread(target=clear_all)
    thread.start()
    print('Почему?')
    return get_close_response()


def rebase():
    print('Пересоздаю таблицы.')
    thread = threading.Thread(target=recreate_all_table())
    thread.start()
    print('Почему?')
    return get_close_response()


def get_word_case(number, key):
    first = number % 10
    second = (number // 10) % 10
    if second == 1:
        return word_case[key][2]
    if first == 1:
        return word_case[key][0]
    if 1 < first < 5:
        return word_case[key][1]
    return word_case[key][2]


def parse_state(state):
    index = state.get('index', 0)
    words = json.loads(state['words'])
    ids = json.loads(state['ids'])

    return index, words, ids
