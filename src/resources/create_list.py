from resources.resource import Resource


class CreateList(Resource):
    def __init__(self):
        super().__init__()
        self._intents = []
