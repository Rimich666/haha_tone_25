import requests
from bs4 import BeautifulSoup


def get_synonyms(word):
    def clear_td(td):
        span = td.find('span')
        if span is not None:
            print(span)
            span.replace_with('')
        return td.get_text()

    url = f"https://sinonim.org/s/{word}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    try:
        table = soup.select('#mainTable .nach')
        return list(filter(lambda s: not not s, [clear_td(td) for td in table]))
    except:
        return None


if __name__ == "__main__":
    print(get_synonyms("очаровательный"))
