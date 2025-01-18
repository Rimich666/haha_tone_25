class Texts:
    def __init__(self, text, tts):
        self._text = text
        self._tts = tts

    def text(self, *args):
        return self._text.format(*args)

    def tts(self, *args):
        return self._tts.format(*args)
