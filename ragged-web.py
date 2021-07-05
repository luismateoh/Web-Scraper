from bs4 import BeautifulSoup
from selenium import webdriver
import time

wd = webdriver.Firefox()

wd.get('https://www.ragged.com.co/menu/33-ropa-mujer#page99')
wd.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(15)
soup = BeautifulSoup(wd.page_source, 'html.parser')
urls = soup.find_all('a', class_="button")

list_hrefs = list()

list_of_products = list()

for n in urls:
    list_hrefs.append(n.get('href'))

count = 0

for url in list_hrefs:

    wd.get(url)
    soup = BeautifulSoup(wd.page_source, 'html.parser')

    list_product = list()

    # name
    name = soup.find_all('h1')[0]
    list_product.append(name.text)

    # Reference
    ref = soup.find_all('p', class_='code')[0]
    list_product.append(ref.text)

    # Price
    price = soup.find_all('p', id='price')[0]
    list_product.append(price.text)

    # Color
    color_list = soup.find_all('input', attrs={"name": "attributes[2]"})
    color = list()
    for c in color_list:
        color.append(c.get('value'))

    list_product.append(color)

    # Size
    size_list = soup.find_all('input', attrs={"name": "attributes[1]"})
    size = list()
    for s in size_list:
        size.append(s.get('value'))

    list_product.append(size)

    # Description
    description = soup.find_all('div', id="tabs")[0].find_all('div', class_="tab")[0]
    description = description.text.replace('\n', '')
    description = description.replace('\t', '')
    list_product.append(description)

    strProduct = str(list_product)
    strProduct = strProduct.replace('[', '')
    strProduct = strProduct.replace(']', '')
    list_of_products.append(strProduct)
    count += 1

    print(count, list_product)

wd.close()

import pandas

df = pandas.DataFrame({"Producto":list_of_products})
df.to_csv('ragged.csv', encoding = 'utf8', index = False)