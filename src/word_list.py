from src.setings import CHECK_IMAGES


def get_word_list(tr):
    return [{'text': item['text'], 'check': False } for item in tr[:5]]


def get_items(words):
    return [
                {
                    "image_id": CHECK_IMAGES[word['check']],
                    "title": word['text'],
                    "description": f'Для установки или отмены выбора назовите индекс: {index}, или просто кликните',
                    "button": {
                        'payload': {'index': index},
                        "text": "Кнопка",
                    }
                } for index, word in enumerate(words)
           ]


def set_check(check_list, words):
    for index in filter(lambda i: i < len(words) ,check_list):
        words[index]['check'] = not words[index]['check']
    return words
