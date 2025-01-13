def get_command(payload, intents):
    if payload:
        mode = payload.get('mode', None)
        if mode:
            return mode
    if intents:
        return list(intents.keys())[0]
