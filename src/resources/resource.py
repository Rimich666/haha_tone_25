from load_resource.load_audio import LoadAudio


class Resource(object):
    def __init__(self):
        self._intents = None
        self.skil = LoadAudio.get_skil()[0]
        self.speaker = 'speaker audio="dialogs-upload'
        self.excellent = '874c6dcf-c804-4d1a-aa5f-e80ac9aad43c'
        self.fail = '6fa4bf54-54e3-4b18-9f41-352112d51b42'
        self.sil = 700

    def check_command(self, command, is_old=None):
        if is_old is None:
            commands = self._intents
        else:
            commands = self._intents.old if is_old else self._intents.new
        return command if command in commands else 'NO_COMMAND'
