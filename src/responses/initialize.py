from repository import base
from setings.setings import first_page_text, mode_images, titles, MODE
from setings.state import State
from resorses import first


def get_start_message(text, tts='', mode=first.mode(True)):
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
                    'description': first_page_text[v],
                    'button': {
                        'payload': {'mode': v},
                        'text': titles[v],
                    }
                } for v in mode
            ]
        }
    }
    if tts:
        rsp['tts'] = tts
    return {'state': State.START}, rsp


def initialize(user_id):
    is_exist = not not base.select_user(user_id).rows
    return get_start_message(first.greeting.old.text(), '', first.mode(is_exist))
