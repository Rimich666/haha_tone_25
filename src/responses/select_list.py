import asyncio
import threading
import time

from helpers import get_word_case
from repository import base
from load_resource.load_audio import LoadAudio
from resources import sources
from setings.state import State

STATE = State().SELECT_LIST


async def load_audio(list_id):
    loader = LoadAudio()

    async def load_file(id, path, audio):
        print(path)
        audio_id = audio if audio else loader.load_file(path)
        res = isProcessed = False
        for _ in range(30):
            isProcessed = loader.get_status(audio_id)
            if isProcessed:
                break
            await asyncio.sleep(0.2)
        if isProcessed:
            res = base.set_audio_id(id, audio_id, is_processed=True)
        return isProcessed and res

    circle = 0
    while True:
        start = time.time()
        circle += 1
        is_created = base.get_created_list(list_id)
        print('is_created:', is_created)
        words_list = base.select_words_list(list_id, False)
        if not words_list:
            break
        print(words_list)

        async with asyncio.TaskGroup() as group:
            tasks = [group.create_task(load_file(w.id, w.file_path, w.audio_id)) for w in words_list]
        # for t in tasks:
        #     t.result()
        # result = sum([t.result() for t in tasks]) / len(tasks) == 1

        print('Круг №', circle, time.time() - start, 'секунд')
        if is_created:
            break
    base.set_list_is_loaded(list_id, True)


def start_load_thread(list_id):
    asyncio.run(load_audio(list_id))


def ready_training(state, rsp):
    # words = {
    #     w['id']:
    #         {
    #             'ru': w['ru'],
    #             'de': w['de'],
    #             'audio_id': w['audio_id'],
    #             'learn': w['learn']
    #         } for w in base.select_words_list(list_id, True)}

    # index = list(words.keys())

    rsp['text'] = sources[STATE].ready.text()
    rsp['tts'] = sources[STATE].ready.tts()

    return state, rsp


def begin_again(state, rsp, list_id):
    base.reset_words_learning(list_id)
    state['full'] = True
    return ready_training(state, rsp)


def resume(state, rsp):
    state['full'] = False
    return state, rsp


def whatever(original, state, rsp):
    state, rsp = begin_again(state, rsp, state['list_id'])
    rsp['text'] = rsp['text'] + sources[STATE].whatever.text(original)
    rsp['tts'] = rsp['tts'] + sources[STATE].whatever.tts(original)
    return state, rsp


def full_or_not(count, leaned, name, state, rsp):
    state['state'] = State.SELECT_LIST
    case = get_word_case(leaned, 'слово')
    rsp['text'] = sources[STATE].full_or_not.text(name, leaned, case, count)
    rsp['tts'] = sources[STATE].full_or_not.tts(name, leaned, case, count)
    return state, rsp


def upload_list(user, name, state, rsp):
    print('select_list')
    list_id, _, count, leaned = base.get_list_info(user, name)

    thread = threading.Thread(target=start_load_thread, args=(list_id,))
    thread.start()

    state['state'] = State.IS_READY
    state['name'] = name
    state['list_id'] = list_id
    state['full'] = True
    return full_or_not(count, leaned, name, state, rsp) if leaned else ready_training(state, rsp)
