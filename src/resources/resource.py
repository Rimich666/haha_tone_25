import abc


class Resource(object):
    def __init__(self):
        self._intents = None

    def check_command(self, command, is_old=None):
        print(command)
        if is_old is None:
            commands = self._intents
        else:
            print(is_old)
            commands = self._intents.old if is_old else self._intents.new
        return command if command in commands else 'NO_COMMAND'
