from repository import base
from responses.initialize import get_start_message
from resorses import first


def not_command(user_id, original):
    is_exist = not not base.select_user(user_id).rows
    texts = first.no_command(is_exist)
    state, rsp = get_start_message(
        texts.text(original),
        texts.tts(original),
        first.mode(is_exist)
    )

    return state, rsp
