from resources.resource import Resource
from resources.texts import Texts


class Hint(Resource):
    def __init__(self):
        super().__init__()
        self._intents = ['NEXT', 'SKIP', 'SPELL', 'SYNONYM', 'HELP']
        self._spell = Texts(
            'Первый слог в этом слове - "{}"',
            'Первый слог в этом слове - "{}"'
        )
        self._synonym = Texts(
            'Синоним этого слова: "{}"',
            'Синоним этого слова: "{}"'
        )

    def spell(self, spell):
        return self._spell.text(spell), self._spell.tts(spell)

    def synonym(self, synonym):
        return self._synonym.text(synonym), self._synonym.tts(synonym)
