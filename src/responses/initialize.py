from repository import base
from setings.setings import descriptions, mode_images, titles, MODE
from setings.state import State


def get_start_message(text, mode=MODE['OLD_USER']):
    return ({'state': State.START},
            {
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
                            'description': descriptions[v],
                            'button': {
                                'payload': {'mode': v},
                                'text': titles[v],
                            }
                        } for v in mode
                    ]
                }
            })


def initialize(user_id):
    is_exist = not not base.select_user(user_id).rows
    key = 'OLD_USER' if is_exist else 'NEW_USER'
    return get_start_message(descriptions['START_TEXT'][key], MODE[key])
