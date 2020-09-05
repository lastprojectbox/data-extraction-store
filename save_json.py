import math
import requests
import json
import re

ip = '34.105.59.26'
proxies = {
    'http': f'http://{ip}:80'
}

page_referer = 0
page_referer += 1
keywords = ('brompton').replace(' ', '%20')
keywords_save = keywords.replace('%20', '_')
country = '.com.my'
url_first = f'https://shopee{country}/api/v2/search_items/?keyword={keywords}'
referer = f'https://shopee{country}/search?keyword={keywords}&page={page_referer}'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'x-shopee-language': 'en',
    'Referer': referer
}

parameters = {
    'by': 'relevancy',
    'limit': '50',
    'newest': '0',
    'order': 'desc',
    'page_type': 'search',
    'version': '2'
}

respons_first = requests.get(url_first, headers=headers, proxies=proxies, params=parameters).json()
list_items = respons_first['items']
total_product_found = respons_first['total_count']

count_page = total_product_found / 50
total_page = math.ceil(count_page)
total_page_real = total_page - 1

data = []
count = 0
newest_count = 0
number = 0

while True:
    url_seconds = f'https://shopee{country}/api/v2/search_items/?by=relevancy&keyword={keywords}&limit=50&newest={newest_count}&order=desc&page_type=search&version=2'
    response_seconds = requests.get(url_seconds, headers=headers, proxies=proxies).json()
    datas = response_seconds['items']
    for data in datas:
        number += 1
        name = data['name']
        namefilter = re.sub('[^A-Za-z0-9]+', '-', name)
        itemid = data['itemid']
        shopid = data['shopid']
        url_product = f'https://shopee{country}/api/v2/item/get?shopid={shopid}'
        referer = f'https://shopee{country}/{namefilter}-i.{shopid}.{itemid}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': referer
        }
        parameters_page = {
            'itemid': itemid,
            'shopid': shopid
        }
        response_third = requests.get(url_product, headers=headers, proxies=proxies, params=parameters_page).json()
        details = response_third['item']
        datas = {
            'name': details['name'],
            'itemid': details['itemid'],
            'shopid': details['shopid'],
            'price': details['price'],
            'price_before_discount': details['price_before_discount'],
            'price_max': details['price_max'],
            'price_max_before_discount': details['price_max_before_discount'],
            'price_min': details['price_min'],
            'price_min_before_discount': details['price_min_before_discount'],
            'discount': details['raw_discount'],
            'stock': details['stock'],
            'liked_count': details['liked_count'],
            'catid': details['catid'],
            'comment_count': details['cmt_count'],
            'historical_sold': details['historical_sold'],
            'shop_location': details['shop_location'],
            'description': details['description'],
            'images': details['images']
        }

        print(f'{number}. {datas}')

        with open('results/{}.json'.format(keywords_save), 'a') as json_file:
            json.dump(datas, json_file)

    if count == total_page_real:
        print(f'\nFinished. Total {number} product has scrapped, from {total_page} pages')
        break
    count += 1
    newest_count = count * 50
