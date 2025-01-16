# pip install git+https://github.com/Koziev/rusyllab

import rusyllab
from typing import List

def extract_first_syllable(word: List[str]) -> str:
        """
    Извлекает первый слог из списка слов с использованием библиотеки `rusyllab`.

    Аргументы:
        words (List[str]): Список слов, из которых нужно извлечь первый слог.

    Возвращает:
        str: Строка, содержащая первый слог первого слова.

    Пример:
        extract_first_syllable(["молоко"])
        'мо'
        extract_first_syllable(["коньки"])
        'конь'
    """
        return rusyllab.split_words(word)[0]
