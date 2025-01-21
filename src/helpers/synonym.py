import requests
from bs4 import BeautifulSoup


def get_synonym(word):
    """
    Получение синонима для русского слова с сайта text.ru.
    """
    url = f"https://sinonim.org/s/{word}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Получаем страницу
    response = requests.get(url, headers=headers)
    html = response.text

    # Парсим HTML
    soup = BeautifulSoup(html, "html.parser")
    # Ищем meta-тег с нужными синонимами
    meta_tag = soup.find("meta", {"name": "description"})
    synonyms = None
    # Извлекаем текст из атрибута content

    if meta_tag:
        synonyms_text = meta_tag["content"]
        # Извлекаем синонимы из текста
        try:
            synonyms = synonyms_text.split(": ")[1].split(", ")[0]
            print(f"Синоним к этому слову — {synonyms}.")
        except IndexError:
            print("Не удалось найти синонимы.")

    return synonyms


if __name__ == "__main__":
    synonyms = get_synonym("вилка")
