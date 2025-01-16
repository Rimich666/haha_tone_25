class Texts:
    def __init__(self, text, tts):
        self._text = text
        self._tts = tts

    def text(self, *args):
        print(args)
        return self._text.format(*args)

    def tts(self, *ars):
        return self._tts.format(*ars)
