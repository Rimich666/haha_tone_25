from setings.setings import descriptions, mode_images, mode, titles
from setings.state import State


def initialize():
    return ({'state': State.START},
            {
                'text': descriptions['START_TEXT'],
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
