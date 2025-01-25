import threading

from load_resource.load_audio import LoadAudio
from repository.queries import select_lists_by_id
from repository.close_queries import select_audio_for_clearn, clear_audio_id


def clear_lists(user_id):
    lists = [item['id'] for item in select_lists_by_id(user_id)[0]]
    if not lists:
        return
    loader = LoadAudio()
    ids, audio_ids = zip(*[(row['id'], row['audio_id']) for row in select_audio_for_clearn(lists)])
    for audio_id in audio_ids:
        loader.delete(audio_id)
    
    clear_audio_id(ids, lists)


def get_close_response(user_id):
    thread = threading.Thread(target=clear_lists, args=(user_id,))
    thread.start()
    print('get_close_response')
    return {
        "version": '1.0',
        "response": {'text': '', 'end_session': True}
    }
