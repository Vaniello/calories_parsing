import os
from datetime import datetime
import json

import requests
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent


def get_response() -> None:
    """
    Get response from server
    Write html into index.html
    :return: None
    """
    ua = UserAgent()
    headers = {
        'accept': '*/*',
        'user-agent': ua.random
    }
    url = 'https://massage.co.ua/uk/tablica-kalorijnosti-produktov-v-100-grammax/'
    resp = requests.get(url=url, headers=headers)
    if not os.path.exists(os.path.join(os.getcwd(), 'data')):  # Check data directory
        os.mkdir(os.path.join(os.getcwd(), 'data'))
    with open(os.path.join(os.getcwd(), 'data', 'index.html'), 'w', encoding='utf-8') as file:  # Write index.html with response
        file.write(resp.content.decode('utf-8'))


def collect_data() -> None:
    """
    Collect calories data and write into json file
    :return: None
    """
    get_response()
    with open(os.path.join(os.getcwd(), 'data', 'index.html'), 'r', encoding='utf-8') as file:
        response = file.read()
    soup = BS(response, 'lxml')
    categories = soup.find('div', class_='blog-ul').find_all('h3')  # Collect all categories
    print(f'Parsing {len(categories)} categories!')
    data = {}  # Empty directory for collected data
    for category in categories:
        category_table = category.next_sibling.next_sibling  # Find category table
        category_name = category.text
        data[category_name] = []  # Products data of current category
        products = category_table.find('tbody').find_all('tr')  # Find all products in category
        for product in products[1:]:
            product_nutrients = product.find_all('td')
            data[category_name].append({
                'product': product_nutrients[0].string.strip(),
                'proteins': product_nutrients[1].string.strip(),
                'fats': product_nutrients[2].string.strip(),
                'carbohydrates': product_nutrients[3].string.strip(),
                'calories': product_nutrients[4].string.strip()
            })
    # Write collected data into json file
    with open(os.path.join(os.getcwd(), 'data', 'content.json'), 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    start_parse = datetime.now()
    collect_data()
    print(f'Collecting complete. Time: {datetime.now() - start_parse}')