from repository import base
from setings.setings import mode_images, titles, card_description
from setings.state import State
from resources import first


def get_start_message(text, tts='', is_old=True):
    cards = first.cards(is_old)
    rsp = {
        'text': text,
        'end_session': False,
        'card': {
            'type': 'ItemsList',
            'header': {
                'text': 'Выберите действие'
            },
            'items': [
                {
                    'image_id': mode_images[v],
                    'title': titles[v],
                    'description': card_description[v],
                    'button': {
                        'payload': {'mode': v},
                        'text': titles[v],
                    }
                } for v in cards
            ]
        }
    }
    if tts:
        rsp['tts'] = tts
    return {'state': State.START}, rsp


def initialize(user_id):
    res = base.select_user(user_id).rows
    id = res[0].id if res else None
    text, tts = first.get_greeting(not not id)
    state, rsp = get_start_message(text, tts, not not id)
    state['user'] = id
    return state, rsp
