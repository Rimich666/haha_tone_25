import asyncio
import json
import threading
import time
from pathlib import Path
from repository import YdbBase, base
from load_resource.load_audio import LoadAudio
from responses.a_initialize import get_start_message
from setings.state import State


async def load_audio(list_id):
    loader = LoadAudio()

    async def load_file(id, path, audio):
        if audio:
            return True
        audio_id = loader.load_file(path)
        res = isProcessed = False
        for _ in range(30):
            isProcessed = loader.get_status(audio_id)
            if isProcessed:
                break
            await asyncio.sleep(1)
        if isProcessed:
            res = base.set_audio_id(id, audio_id)
        return isProcessed and res

    start = time.time()
    print("Loading start", start)

    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(load_file(w.id, w.file_path, w.audio_id)) for w in base.select_words_list(list_id)]
    result = sum([t.result() for t in tasks]) / len(tasks) == 1
    base.set_list_is_loaded(list_id, result)
    finish = time.time()
    print("Loading finish", finish)
    print("Loading time", finish - start)


def start_load_thread(list_id):
    asyncio.run(load_audio(list_id))


def get_is_loaded(list_id, name):
    words = {w['id']: {'ru': w['ru'], 'de': w['de'], 'audio_id': w['audio_id']} for w in
             base.select_words_list(list_id)}
    index = list(words.keys())

    return (
        {
            'state': State.IS_LOADED,
            'name': name,
            'list_id': list_id,
            'words': json.dumps(words),
            'ids': json.dumps(index)
        },
        {'text': f'Список {name} готов к работе'})


def check_load_list(state, rsp):
    list_id, name = state["list_id"], state['name']
    id, is_loaded = base.get_list_is_loaded(list_id)
    if not id:
        state, rsp = get_start_message(f'Произошёл непредвиденный сбой, индекс списка {name} не найден')
        return {'state': State.START}, rsp

    if is_loaded is None:
        return {'state': State.SELECT_LIST, 'name': name, 'list_id': list_id}, {'text': f'Список {name} загружается'}

    if is_loaded:
        return get_is_loaded(list_id, name)


def upload_list(user, name):
    print('select_list')
    list_id, is_loaded = base.get_list_id(user, name)

    if not list_id:
        state, rsp = get_start_message(f'У вас нет списка с именем {name}')
        return {'state': State.START}, rsp

    if is_loaded:
        return get_is_loaded(list_id, name)

    thread = threading.Thread(target=start_load_thread, args=(list_id,))
    thread.start()
    return {'state': State.SELECT_LIST, 'name': name, 'list_id': list_id}, {'text': f'Загружаю список {name}'}


if __name__ == '__main__':
    l_id = 1
    nm = 'майский зелёный'
    pth = Path.joinpath(Path(__file__).parents[2], 'test_data')
    original = Path.joinpath(pth, 'original.json')
    bs = YdbBase()
    wrds = {w['id']: {'ru': w['ru'], 'de': w['de'], 'audio_id': w['audio_id']} for w in
            bs.select_words_list(l_id)}
    ndx = list(wrds.keys())

    stt = {
        'state': State.IS_LOADED,
        'name': nm,
        'list_id': l_id,
        'words': wrds,
        'ids': ndx
    }
    with open(original, 'w') as file:
        json.dump(stt, file)

    print(pth)
    pass
