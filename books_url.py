import requests
from parsel import Selector
from price_parser import Price
import pandas as pd

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'priority': 'u=0, i',
    'referer': 'https://www.google.com/',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
}

response = requests.get('https://books.toscrape.com/',
                        headers=headers, )
resp = Selector(response.text)

books = []
element = resp.css('.product_pod')
for e in element:
    name = e.css('h3 ::attr("title")').get()
    price = e.css('.price_color ::text').get()
    price = Price.fromstring(price)
    rel_url = e.css('h3 a ::attr("href")').get()
    url = 'https://books.toscrape.com/' + rel_url
    book = {
        'name': name,
        'url': url,
        'alert_price': price.amount_float,
    }
    books.append(book)
print(books[0:3])
data = pd.DataFrame(books)
print(type(data))
print(data.head())
data.to_csv('./products.csv')
