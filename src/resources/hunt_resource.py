from resources.resource import Resource


class Hint(Resource):
    def __init__(self):
        super().__init__()
        self._intents = ['NEXT', 'SKIP', 'SPELL', 'SYNONYM']
