from resources.resource import Resource
from resources.texts import Texts


class Hint(Resource):
    def __init__(self):
        super().__init__()
        self._intents = ['NEXT', 'SKIP', 'SPELL', 'SYNONYM', 'HELP', 'STOP']
        self._spell = Texts(
            'Первый слог в этом слове - "{}"',
            'Первый слог в этом слове - "{}"'
        )
        self._synonym = Texts(
            'Синоним этого слова: "{}"',
            'Синоним этого слова: "{}"'
        )
        self._help = Texts(
            '''
            Вы можете пропустить слово, или прекратить тренинг.
            Вам доступны подсказки: "Дай синоним", "Подскажи первый слог" 
            ''',
            '''
            Вы можете пропустить слово, или прекратить тренинг.
            Вам доступны подсказки: "Дай синоним", "Подскажи первый слог" 
            '''
        )

    def spell(self, spell):
        return self._spell.text(spell), self._spell.tts(spell)

    def synonym(self, synonym):
        return self._synonym.text(synonym), self._synonym.tts(synonym)
