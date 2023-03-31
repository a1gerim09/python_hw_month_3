from pprint import pprint

import requests
from bs4 import BeautifulSoup


URL = 'https://rezka.ag/animation/'

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}


def get_html(url):
    response = requests.get(url=url, headers=HEADERS)
    return response


def get_data_from_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all(
        'div', class_="b-content__inline_item"
    )
    animation = []
    for item in items:
        info = item.find('div', class_="b-content__inline_item-link").find('div').getText().split(', ')
        anime = {
            'title': item.find('div', class_="b-content__inline_item-link").find('a').getText(),
            'link': item.find('div', class_="b-content__inline_item-link").find('a').get('href'),
            'year': info[0],
            'country': info[1],
            'genre': info[2]
        }
        animation.append(anime)
    return animation


def parser():
    html = get_html(URL)
    if html.status_code == 200:
        animation = []
        for i in range(1, 2):
            html = get_html(f"{URL}page/{i}/")
            current_page = get_data_from_page(html.text)
            animation.extend(current_page)
        return animation
    else:
        raise Exception("Error in parser")




