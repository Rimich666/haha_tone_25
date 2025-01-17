import random
import threading

from load_resource.load_audio import LoadAudio
from repository import base
from repository.object_store import ObjectStore


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
    return {
        "version": '1.0',
        "response": {'text': '', 'end_session': True}
    }


def create_list_name(user, name):
    lists, user_id = base.select_lists(user)
    names = [i.name for i in lists]
    if name == '' or name in names:
        free_names = base.select_free_names(names)
        return free_names[random.randrange(len(free_names))], user_id
    return name, user_id


def clear_all():
    # words = base.select_all_words()
    store = ObjectStore()
    loder = LoadAudio()
    ids = base.select_all_audio()
    if ids:
        for id in [i['audio_id']for i in ids]:
            loder.delete(id)
    store.delete()
    base.clear_tables()


def reset():
    thread = threading.Thread(target=clear_all)
    thread.start()
    return get_close_response()
