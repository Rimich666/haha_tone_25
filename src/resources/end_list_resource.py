from resources.resource import Resource


class EndList(Resource):
    def __init__(self):
        super().__init__()
        self._intents = ['NO', 'FIX', 'ANOTHER']
