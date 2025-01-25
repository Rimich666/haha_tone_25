import asyncio
import threading
import time

from helpers.helpers import get_word_case
from load_resource.load_audio import LoadAudio
from repository.queries import get_list_info, reset_words_learning, set_list_is_loaded, set_audio_ids, \
    select_words_list, get_created_list
from resources import sources
from setings.state import State

STATE = State().SELECT_LIST


async def load_audio(list_id):
    loader = LoadAudio()

    async def load_file(id, path, audio):
        audio_id = audio if audio else loader.load_file(path)
        is_processed = False
        for _ in range(30):
            is_processed = loader.get_status(audio_id)
            if is_processed:
                break
            await asyncio.sleep(0.3)
        return id, audio_id, is_processed

        if is_processed:
            return id, audio_id
            res = base.set_audio_id(id, audio_id, is_processed=True)
        return is_processed and res

    circle = 0
    while True:
        start = time.time()
        await asyncio.sleep(circle)
        circle += 1
        is_created = get_created_list(list_id)
        print('\033[32m', 'is_created:', is_created, '\033[0m')
        words_list = select_words_list(list_id, False)
        if not words_list:
            if is_created:
                break
            continue
        print('\033[32m', words_list, '\033[0m')
        async with asyncio.TaskGroup() as group:
            tasks = [group.create_task(load_file(w.id, w.file_path, w.audio_id)) for w in words_list]
        result = [t.result() for t in tasks]
        print(result)
        if result:
            set_audio_ids(result)

        print('\033[32m', 'Круг №', circle, time.time() - start, 'секунд', '\033[0m')
        if is_created:
            break
    set_list_is_loaded(list_id, True)


def start_load_thread(list_id):
    asyncio.run(load_audio(list_id))


def ready_training(state, rsp, name):
    state['state'] = State.IS_READY
    rsp['text'] = sources[STATE].ready.text(name)
    rsp['tts'] = sources[STATE].ready.tts(name)

    return state, rsp


def begin_again(state, rsp, list_id):
    reset_words_learning(list_id)
    return ready_training(state, rsp, state['name'])


def resume(state, rsp):
    return ready_training(state, rsp, state['name'])


def whatever(original, state, rsp):
    state, rsp = begin_again(state, rsp, state['list_id'])
    rsp['text'] = sources[STATE].whatever.text(original) + rsp['text']
    rsp['tts'] = sources[STATE].whatever.tts(original) + rsp['tts']
    return state, rsp


def full_or_not(count, leaned, name, state, rsp):
    state['state'] = State.SELECT_LIST
    case = get_word_case(leaned, 'слово')
    rsp['text'] = sources[STATE].full_or_not.text(name, leaned, case, count)
    rsp['tts'] = sources[STATE].full_or_not.tts(name, leaned, case, count)
    return state, rsp


def upload_list(user, name, state, rsp):
    print('select_list')
    list_id, _, count, learned = get_list_info(user, name)
    print(learned)
    thread = threading.Thread(target=start_load_thread, args=(list_id,))
    thread.start()

    state['state'] = State.IS_READY
    state['name'] = name
    state['list_id'] = list_id
    return full_or_not(count, learned, name, state, rsp) if learned else ready_training(state, rsp, name)
