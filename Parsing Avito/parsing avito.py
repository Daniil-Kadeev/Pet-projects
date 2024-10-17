from selectolax.parser import HTMLParser
import requests
from urllib.parse import unquote
import json
from datetime import datetime


SITE = r'https://www.avito.ru'

def get_json(url):
    response = requests.get(url=url)
    html = response.text
    tree = HTMLParser(html)
    items = tree.css('div[data-marker="item"]')
    skripts = tree.css('script')

    for skript in skripts:
        # нашли джесон файл из которого грузатся данные на сайт
        # как найти: зайти в исходный код страницы ctrl+U и искать непонятные знаки
        if 'window.__initialData__' in skript.text():
            json_text = skript.text().split(';')[0].split('=')[-1].strip()
            json_text = unquote(json_text)
            data = json.loads(json_text[1:-1])
    return data


def get_offers(data):
    # байдень которую нужно вылавливать из джейсон файла
    offers = list()
    for key in data:
        if 'single-page' in key:
            items = data[key]['data']['catalog']['items']
            for item in items:
                if item.get('id'):
                    offer = dict()
                    offer['price'] = item['priceDetailed']['value']
                    offer['title'] = item['title'].split(r',')
                    offer['city'] = item['geo']['geoReferences'][0]['content']
                    offer['address'] = item['geo']['formattedAddress']
                    offer['url'] = SITE + item['urlPath']
                    timestamp = datetime.fromtimestamp(item['sortTimeStamp'] / 1000)
                    timestamp = datetime.strftime(timestamp, '%d.%m.%Y at %H:%M')
                    offer['date'] = timestamp
                    offers.append(offer)
    return offers


def main():
    url = r'https://www.avito.ru/moskva/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?context=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYyNLNSKk5NLErOcMsvyg3PTElPLVGyrgUEAAD__xf8iH4tAAAA&s=104'
    data = get_json(url)
    get_offers(data)


if __name__ == '__main__':
    main()

