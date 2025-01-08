import string
from functools import reduce


class Alfabet(object):
    de = 0
    ru = 1
    undefined = 2
    punctuation = string.punctuation + string.digits + '\r'

    def __init__(self):
        self.a = ord('a')
        self.z = ord('z')
        self.A = ord('A')
        self.Z = ord('Z')
        self.ext_de = 'ÄäÖöÜüß '
        self.rA = ord('А')
        self.rya = ord('я')
        self.ext_ru = 'ёЁ '
        self.deleted = str.maketrans("", "", Alfabet.punctuation)

    def is_ru(self, let):
        return (self.rA <= ord(let) <= self.rya) or (let in self.ext_ru)

    def is_de(self, let):
        return (self.A <= ord(let) <= self.Z) or (self.a <= ord(let) <= self.z) or (let in self.ext_de)

    def check(self, word, lang, first_letter=True):
        check_let = self.is_de if lang == Alfabet.de else self.is_ru

        if first_letter:
            return check_let(word[0])
        else:
            res = reduce(lambda acc, cur: acc and check_let(cur), list(word), True)
            return res

    def get_lang(self, word):
        if self.check(word, Alfabet.de):
            return Alfabet.de
        if self.check(word, Alfabet.ru):
            return Alfabet.ru
        return Alfabet.undefined

    def trans(self, word):
        return word.translate(self.deleted)


if __name__ == '__main__':
    print(string.punctuation + string.digits + '\r')
    print(string.printable)
    print(string.digits)
