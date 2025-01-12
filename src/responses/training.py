import json
import random

from load_resource.load_audio import LoadAudio
from setings.setings import SPEAKER, EXCELLENT, FAIL, SIL, descriptions
from setings.state import State


def send_word(state, rsp, answer=None):
    def end_list():
        state.pop('index', None)
        state['state'] = State.END_LIST
        state['ids'] = json.dumps(list(map(int, words.keys())))
        rsp['tts'] = descriptions['END_LIST']
        rsp['text'] = descriptions['END_LIST']
        return state, rsp

    def check_answer():
        index = state['index']
        right = words[str(ids[index])]['ru'].split(' ')
        is_subset = set(right).issubset(answer)
        print(ids)
        if is_subset:
            ids.pop(index)
        return f'<{SPEAKER}/{skil}/{EXCELLENT if is_subset else FAIL}.opus"> sil <[{SIL}]>'

    def next_word():
        index = 0 if count == 1 else random.randrange(count)
        print(len(ids), ids, index)

        word = words[str(ids[index])]
        state['index'] = index
        state['state'] = State.QUESTION
        state['ids'] = json.dumps(ids)
        tts = f'{grade} <{SPEAKER}/{skil}/{word['audio_id']}.opus">'
        rsp['text'] = f"{word['de']}: {word['ru']}"
        rsp['tts'] = tts
        print(tts)
        return state, rsp

    skil = LoadAudio.get_skil()[0]
    words = json.loads(state['words'])
    # words = state['words']
    ids = json.loads(state['ids'])
    # ids = state['ids']
    grade = check_answer() if answer else ''
    print('grade:', grade)
    count = len(ids)

    if count == 0:
        return end_list()

    return end_list() if count == 0 else next_word()


if __name__ == "__main__":
    from pathlib import Path
    path = Path.joinpath(Path(__file__).parents[2], 'test_data')
    original = Path.joinpath(path, 'original.json')
    current = Path.joinpath(path, 'current.json')

    while True:
        with open(current, 'r') as f:
            file = f.read()
            obj = json.loads(file)

        ids = obj['ids']
        words = obj['words']
        word = words[str(ids[obj['index']])] if 'index' in obj else {'ru': ''}
        ans = word['ru'].split(' ') if word['ru'] else None
        state, rsp = send_word(obj, {}, ans)
        with open(current, 'w') as file:
            json.dump(state, file)
        if state['state'] == State.END_LIST:
            break
    print(rsp, state['state'])
