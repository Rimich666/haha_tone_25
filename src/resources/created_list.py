from resources.resource import Resource


class CreatedList(Resource):
    def __init__(self):
        super().__init__()
        self._intents = ['YES', 'NO']
