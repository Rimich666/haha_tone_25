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
        self._not_understand = Texts(
            'Подсказать первый слог или синоним?',
            'Извините, вынуждена переспросить. Вам подсказать первый слог? Дать синоним? Или пропустить слово?'
        )

    def spell(self, spell):
        return self._spell.text(spell), self._spell.tts(spell)

    def synonym(self, synonym):
        return self._synonym.text(synonym), self._synonym.tts(synonym)

    def not_understand(self):
        return self._not_understand.text(), self._not_understand.tts()