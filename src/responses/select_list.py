import asyncio
import json
import threading
import time
from pathlib import Path
from repository import YdbBase, base
from load_resource.load_audio import LoadAudio
from setings.state import State


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
        print(words_list)

        async with asyncio.TaskGroup() as group:
            tasks = [group.create_task(load_file(w.id, w.file_path, w.audio_id)) for w in words_list]
        result = sum([t.result() for t in tasks]) / len(tasks) == 1
        base.set_list_is_loaded(list_id, result)
        print('Круг №', circle, time.time() - start, 'секунд')
        if is_created:
            break


def start_load_thread(list_id):
    asyncio.run(load_audio(list_id))


# def get_is_loaded(list_id, name):
#     words = {w['id']: {'ru': w['ru'], 'de': w['de'], 'audio_id': w['audio_id']} for w in
#              base.select_words_list(list_id)}
#     index = list(words.keys())
#
#     return (
#         {
#             'state': State.IS_LOADED,
#             'name': name,
#             'list_id': list_id,
#             'words': json.dumps(words),
#             'ids': json.dumps(index)
#         },
#         {'text': f'Список {name} готов к работе'})


# def check_load_list(state, rsp):
#     list_id, name = state["list_id"], state['name']
#     id, is_loaded = base.get_list_is_loaded(list_id)
#     if not id:
#         state, rsp = get_start_message(f'Произошёл непредвиденный сбой, индекс списка {name} не найден')
#         return {'state': State.START}, rsp
#
#     if is_loaded is None:
#         return {'state': State.SELECT_LIST, 'name': name, 'list_id': list_id}, {'text': f'Список {name} загружается'}
#
#     if is_loaded:
#         return get_is_loaded(list_id, name)


def upload_list(user, name):
    print('select_list')
    list_id, is_loaded = base.get_list_id(user, name)

    thread = threading.Thread(target=start_load_thread, args=(list_id,))
    thread.start()

    words = {w['id']: {'ru': w['ru'], 'de': w['de'], 'audio_id': w['audio_id']} for w in
             base.select_words_list(list_id, True)}
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

    # return {'state': State.SELECT_LIST, 'name': name, 'list_id': list_id}, {'text': f'Загружаю список {name}'}


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
