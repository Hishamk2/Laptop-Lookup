import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import random
import time
import json

all_laptops_counter = 0
all_laptops = {}
# TODO maybe have the price and the currency

print("Start of the program\n")

def get_total_num_pages(total_num_results, num_results_per_page):
    return round(int(total_num_results) / int(num_results_per_page))

def get_total_num_results(result_range):
    result_range_string = result_range.text
    start_index = result_range_string.find("of ") + 3
    for i in range(start_index, len(result_range_string)):
        if not result_range_string[i].isdigit():
            return result_range_string[start_index:i].strip()

def get_result_range(soup):
    result_range = soup.find(class_="pageinfo")
    return result_range

def get_num_results_per_page(result_range):
    dash_index = result_range.text.find("-")
    lots = result_range.text[dash_index + 1:].strip()
    return_val = ""
    for ea_char in lots:
        if ea_char.isdigit():
            return_val += ea_char
        else:
            return return_val

# TODO Make it so that it also adds teh currency
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

def get_laptop_names(soup):
    laptop_name = []
    laptop_name_html = []
    laptop_name_html = soup.findAll(class_="ps-title")
    for name in laptop_name_html:
        name_text = name.text.strip()
        laptop_name.append(name_text)
    return laptop_name

def get_laptop_processor(soup):
    laptop_processor = []
    laptop_processor_html = []
    laptop_processor_html = soup.findAll(
        class_="ps-iconography-container ps-icon-specs-container")
    for processor in laptop_processor_html:
        processor_text = processor.find(
            class_="ps-iconography-specs-label").text.strip()
        laptop_processor.append(processor_text)
    return laptop_processor

def get_laptop_ram(soup):
    laptop_ram = []
    laptop_ram_html = []
    laptop_ram_html = soup.findAll(
        class_="ps-iconography-container ps-icon-specs-container")
    for ram in laptop_ram_html:
        ram_text = ram.findAll(
            class_="ps-iconography-specs-label")[-3].text.strip()
        laptop_ram.append(ram_text)
    return laptop_ram

def merge_lists(sale_type, names, prices, processors, rams, links, GPUs, storage, sale, all_laptops):
    laptop = {}
    for i in range(0, len(names)):
        laptop = {'Link' : links[i], 'Name' : names[i], 'Original Price' : sale[i], 'Sale Type' : sale_type[i], 'Price' : prices[i], 'Processor' : processors[i], 'GPU:' : GPUs[i], 'RAM' : rams[i], 'Storage' : storage[i]}
        global all_laptops_counter
        all_laptops[all_laptops_counter] = laptop
        all_laptops_counter += 1
    return all_laptops

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

def get_laptop_link(soup):
    laptop_link = []
    laptop_link_html = []
    # fix, prob make it first find above class then this class etc
    laptop_link_html = soup.findAll(class_="ps-show-hide-bottom")
    for link in laptop_link_html:
        x = link.find(class_="ps-button ps-button-system-details")
        if x != None:
            y = x.find(class_="ps-btn ps-blue")
            link_text = y.get('href')
            laptop_link.append(link_text)
        else:
            x = link.find(class_="ps-button ps-button-details")
            y = x.find(class_="ps-btn ps-blue")
            link_text = y.get('href')
            laptop_link.append(link_text)
    return laptop_link

def get_laptop_GPU(soup):
    laptop_GPU = []
    laptop_GPU_html = []
    laptop_GPU_html = soup.findAll(class_="ps-iconography-container ps-icon-specs-container")
    for gpu in laptop_GPU_html:
        GPU_one_above = gpu.find(class_="ps-iconography-icons video-card")
        if GPU_one_above != None:
            GPU_text = GPU_one_above.next_sibling.next_sibling.text.strip()
            laptop_GPU.append(GPU_text)
        else:
            laptop_GPU.append("N/A")
    return laptop_GPU

def get_laptop_storage(soup):
    laptop_storage = []
    laptop_storage_html = []
    laptop_storage_html = soup.findAll(class_="ps-iconography-container ps-icon-specs-container")
    for storage in laptop_storage_html:
        storage_text_one_above = storage.find(class_="ps-iconography-icons hard-drive")
        if storage_text_one_above != None:
            storage_text = storage_text_one_above.next_sibling.next_sibling.text.strip()
            laptop_storage.append(storage_text)
        else:
            laptop_storage.append("N/A")
    return laptop_storage

def get_all_laptop_info(soup):
    laptop_names = get_laptop_names(soup)
    laptop_prices = get_laptop_prices(soup)
    laptop_processor = get_laptop_processor(soup)
    laptop_ram = get_laptop_ram(soup)
    laptop_links = get_laptop_link(soup)
    laptop_GPU = get_laptop_GPU(soup)
    laptop_storage = get_laptop_storage(soup)
    laptop_sale = get_original_price(soup)
    laptop_sale_type = get_sale_type(soup)
    global all_laptops
    all_laptops = merge_lists(laptop_sale_type, laptop_names, laptop_prices, laptop_processor, laptop_ram, laptop_links, laptop_GPU, laptop_storage, laptop_sale, all_laptops)
    return all_laptops


def get_original_price(soup):
    original_price = []
    original_price_html = []
    original_price_html = soup.findAll(class_='ps-pricing-container-without-promotions')
    count = 0
    for price in original_price_html:
        if (count % 2 == 0):
            x = price.find(class_='ps-orig ps-simplified')
            if x != None:
                y = x.find(class_='strike-through')
                original_price_text = y.text.strip()
                # original_price_text = remove_extra_stuff(original_price_text)
                original_price.append(original_price_text)
            else:
                original_price.append("Not on sale")
        count += 1
    return original_price

def get_sale_type(soup):
    sale_type = []
    sale_type_html = []
    sale_type_html = soup.findAll(class_='ps-top')
    for sale in sale_type_html:
        x = sale.find(class_='ps-promo-text')
        if x != None:
            sale_text = x.text.strip()
            sale_type.append(sale_text)
        else:
            sale_type.append("Not on sale")
    return sale_type

# URL = """
# https://www.dell.com/en-ca/search/laptop?sb=pricing.saleprice,asc&p=1&t=Product&r=37654
# """
i = 1
URL = f'https://www.dell.com/en-ca/search/laptop?r=37654&p={i}&t=Product'

with open("DellHTML(2).html", encoding='utf-8') as fp:
    soup = BeautifulSoup(fp, 'html.parser')

all_laptops = get_all_laptop_info(soup)

# with open("DellHTML(23).json", "w") as f:
#     json.dump(all_laptops, f, indent=4)

path = extract_suffix(URL)
headers = [
    {
        "authority": "www.dell.com",
        "method": "GET",
        "path": path,
        "scheme": "https",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Priority": "u=0, i",
        "Sec-Ch-Ua": '''"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"''',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Sec-Gpc": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    },
    {
        "authority": "www.dell.com",
        "method": "GET",
        "path": path,
        "scheme": "https",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Priority": "u=0, i",
                    "Sec-Ch-Ua": '''"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"''',
                    "Sec-Ch-Ua-Mobile": "?0",
                    "Sec-Ch-Ua-Platform": '"Windows"',
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-User": "?1",
                    "Sec-Gpc": "1",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"
    },
    {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-CA,en-US;q=0.7,en;q=0.3",
        "Connection": "keep-alive",
        "DNT": "1",
        "Host": "www.dell.com",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "TE": "trailers",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"
    }
]

# response = requests.get(URL, headers=headers[random.randint(0, len(headers) - 1)], timeout=10)
# soup = BeautifulSoup(response.content, 'html.parser')

# result_range = get_result_range(soup)
# num_results_per_page = get_num_results_per_page(result_range)
# total_num_results = get_total_num_results(result_range)
# total_num_pages = get_total_num_pages(total_num_results, num_results_per_page)

# for i in range(1, total_num_pages + 1):
#     URL = f'https://www.dell.com/en-ca/search/laptop?r=37654&p={i}&t=Product'
#     time.sleep(20)
#     if i != 1:
#         response = requests.get(URL, headers=headers[random.randint(0, len(headers) - 1)], timeout=10)
#         soup = BeautifulSoup(response.content, 'html.parser')

#     all_laptops = get_all_laptop_info(soup)


for i in range(0, len(all_laptops)):
    print(all_laptops[i], "\n")
    
# TODO prrob can make the program better by iterating through each div container containing each laptop like in the AcerScraper.py file
print("\nEnd of the program")

# i3 https://www.dell.com/en-ca/search/laptop?r=37654&p=1&ac=facetselect&t=Product
# i5 https://www.dell.com/en-ca/search/laptop?r=37653&p=1&ac=facetselect&t=Product
