from bs4 import BeautifulSoup
import random

# URL = 'https://www.dell.com/en-ca/search/laptop?r=37654,37789&p=1&ac=facetselect&t=Product'
# print(URL.lower().find("www."))
# print(URL[URL.lower().find("www.") + len("www."):])
# prefix = URL[URL.lower().find("www.") + len("www."): URL[URL.lower().find("www.") + len("www."):].lower().find("/") + len("/") + len(URL[URL.lower().find("www.") + len("www."):])]
# print("prefix", prefix)
# path = URL[URL.lower().find(prefix) + len(prefix):]
# UA_path = "/en-ca/search/laptop?r=37654,37789&p=1&ac=facetselect&t=Product"


from urllib.parse import urlparse


def extract_suffix(url):
    parsed_url = urlparse(url)
    suffix = parsed_url.path
    if parsed_url.query:
        suffix += '?' + parsed_url.query
    if parsed_url.fragment:
        suffix += '#' + parsed_url.fragment
    if parsed_url.params:
        suffix += ';' + parsed_url.params
    return suffix


# Example usage:
# url = "https://www.dell.ca/en-ca/search/laptop?r=37654,37789&p=1&ac=facetselect&t=Product"
# suffix = extract_suffix(url)
# print("Suffix:", suffix)
# print(type(extract_suffix(url)))


# print(URL)
# print(path)
# print(path == UA_path)


with open("DellHTML(516).html", encoding='utf-8') as fp:
    soup = BeautifulSoup(fp, 'html.parser')

def get_laptop_prices(soup):
    laptop_price = []
    laptop_price_html = []
    laptop_price_html = soup.findAll(class_="ps-dell-price ps-simplified")
    count = 0
    # Two prices are shown for each laptop, so we only want to get the first one (both are the same prices though)
    # First price is in class "ps-show-hide" and second price is in class "ps-show-hide-bottom"
    # TODO Check just one of the classes so don't have to do the count % 2 == 0
    for price in laptop_price_html:
        if (count % 2 == 0):
            price_text = price.text.strip()
            price_text = remove_extra_stuff(price_text)   
            laptop_price.append(price_text)
        count += 1
    return laptop_price

def remove_extra_stuff(price):
    # Remove the extra stuff from the price
    # Extra stuff is anything that doesn't fit the format of a price
    # Format of a a correct price is $1,234.56
    for char in price:
        if not char.isdigit() and char != "." and char != ",":
            price = price.replace(char, "")
    return price

laptop_price = get_laptop_prices(soup)


print("\n", laptop_price)

i = 1
x = f'testing{i}dasdas'

for i in range(10):
    x = f'testing{i}dasdas'
    print(x)