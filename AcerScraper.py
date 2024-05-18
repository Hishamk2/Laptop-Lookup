import time

start_time = time.time()

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import random
import time
import json

# TODO learn to implement classes
# TODO esp so I can use the remove_extra_stuff function in this file


    
def prints(list):
    for item in list:
        print(item)

def convert_to_lowercase(list):
    new_list = []
    for i in range(0, len(list)):
        new_list.append(list[i].lower())
    return new_list

# paramater has to be lowercase
def find_laptop_processor_index(list):
    intel_processor_names = ['core', 'celeron', 'pentium', 'atom', 'xeon', 'itanium']
    amd_processor_names = ["ryzen", "athlon", "duron", "turion", "phenom", "a-series", "e-series", "fx-series", "opteron", "threadripper", "sempron"]

    for index in range(0, len(list)):
        if 'processor' in list[index]:
            return index
        elif ('intel' in list[index]): 
            for processor_name in intel_processor_names:
                if processor_name in list[index]:
                    return index # important to return index here and not afterwards as a GPU could be mistaken for a processor if the name for that gpu is intel (ie intel graphics)
        elif ('amd' in list[index]):
            for processor_name in amd_processor_names:
                if processor_name in list[index]:
                    return index
    return -1

def get_laptop_processor(laptop_html):
    laptop_info = laptop_html.find(class_='clearfix').text.strip().split('\n')
    laptop_info_lower = convert_to_lowercase(laptop_info)
    processor_index = find_laptop_processor_index(laptop_info_lower)
    if processor_index == -1:
        return "N/A"
    else:
        return laptop_info[processor_index]

def find_laptop_ram_index(list):
    for index in range(0, len(list)):
        # order matters as fsm acer has smthn like this for some: '4 gb standard memory; 32 gb flash storage' on one line
        if 'ram' in list[index]:
            return index
        elif 'standard memory' in list[index]:
            return index
        elif 'ddr4' in list[index]:
            return index
        elif 'ddr5' in list[index]:
            return index
        elif 'flash' in list[index] and 'memory' in list[index]:
            continue
    return -1
        
def get_laptop_ram(laptop_html):
    laptop_info = laptop_html.find(class_='clearfix').text.strip().split('\n')
    laptop_info_lower = convert_to_lowercase(laptop_info)
    ram_index = find_laptop_ram_index(laptop_info_lower)
    if ram_index == -1:
        return "N/A"
    else:
        return laptop_info[ram_index]


def just_gb(string_laptop_info):
    no_numbers = ''
    for char in string_laptop_info:
        if not char.isdigit():
            no_numbers += char
    no_numbers = no_numbers.strip().lower()
    if 'gb' == no_numbers:
        return True
    return False


def find_laptop_storage_index(list):
    # use above as reference
    for index in range(0, len(list)):
        if 'flash storage' in list[index]:
            return index
        elif 'flash memory' in list[index]:
            return index
        elif 'ssd' in list[index]:
            return index
        elif just_gb(list[index]):
            return index
        elif 'flash' in list[index] and 'storage' in list[index]:
            return index
        elif 'solid state drive' in list[index]:
            return index
        elif 'hard disk drive' in list[index]:
            return index
        elif 'hdd' in list[index]:
            return index
        
        if (('flash storage' in list[index]) or 
            ('flash memory' in list[index]) or 
            ('ssd' in list[index]) or 
            (just_gb(list[index])) or 
            ('flash' in list[index] and 'storage' in list[index]) or 
            ('solid state drive' in list[index]) or 
            ('hard disk drive' in list[index]) or 
            ('hdd' in list[index])):
            return index

    return -1
        
def get_laptop_storage(laptop_html):
    laptop_info = laptop_html.find(class_='clearfix').text.strip().split('\n')
    laptop_info_lower = convert_to_lowercase(laptop_info)
    storage_index = find_laptop_storage_index(laptop_info_lower)
    if storage_index == -1:
        return "N/A"
    else:
        return laptop_info[storage_index]
    
# TODO fix this, doesnt work for discounted price
def get_laptop_price(laptop_html):
    price = laptop_html.find(class_='price-wrapper', attrs={'data-price-type' : 'finalPrice'}).text.strip()
    return price


def remove_extra_stuff(price):
    # Remove the extra stuff from the price
    # Extra stuff is anything that doesn't fit the format of a price
    # Format of a a correct price is $1,234.56
    for char in price:
        if not char.isdigit() and char != "." and char != ",":
            price = price.replace(char, "")
    return price

def merge_lists(links, names, prices, processors, rams, gpus, storages, old_prices, sale_types):
    laptop = {}
    all_laptops = {}
    for i in range(0, len(links)):
        laptop = {'Link' : links[i], 'Name' : names[i], 'Sale Type' : sale_types[i],'Old Price' : old_prices[i],'Price' : prices[i], 'Processor' : processors[i], 'GPU' : gpus[i], 'RAM' : rams[i], 'Storage' : storages[i]}
        all_laptops[i] = laptop
    return all_laptops


def find_laptop_gpu_index(list):
    for index in range(0, len(list)):
        if 'graphics' in list[index]:
            return index
        elif 'dedicated' in list[index] and 'memory' in list[index]:
            return index
        elif 'gpu' in list[index]:
            return index
    return -1

def get_laptop_GPU(laptop_html):
    laptop_info = laptop_html.find(class_='clearfix').text.strip().split('\n')
    laptop_info_lower = convert_to_lowercase(laptop_info)
    gpu_index = find_laptop_gpu_index(laptop_info_lower)
    if gpu_index == -1:
        return "N/A"
    else:
        return laptop_info[gpu_index]


def get_laptop_sale_type(laptop_html):
    sale_type = laptop_html.find(class_="sales-label promotion-sales-label")
    if sale_type == None:
        return "Not on sale"
    else:
        return sale_type.text.strip()

def get_laptop_old_price(laptop_html):
    price_html = laptop_html.find(class_='price-wrapper', attrs={'data-price-type' : 'oldPrice'})
    if price_html == None:
        return 'Not on sale'
    else:
        price = remove_extra_stuff(price_html.text.strip())
        return price


with open("AcerHTML(106).html", encoding='utf-8') as fp:
    soup = BeautifulSoup(fp, 'html.parser')

laptop_names = []
laptop_links = []
laptop_prices = []
laptop_processor = []
laptop_ram = []
laptop_storage = []
laptop_gpu = []
laptop_old_prices = []
laptop_sale_type = []

all_laptop_info_html = soup.findAll(class_="item product product-item")


for laptop in all_laptop_info_html:
    laptop_name = laptop.find(class_="product name product-item-name")
    laptop_names.append(laptop_name.text.strip())
    laptop_links.append(laptop_name.find(class_='product-item-link').get('href'))
    laptop_processor.append(get_laptop_processor(laptop))
    laptop_ram.append(get_laptop_ram(laptop))
    laptop_storage.append(get_laptop_storage(laptop))
    laptop_prices.append(remove_extra_stuff(get_laptop_price(laptop)))
    laptop_gpu.append(get_laptop_GPU(laptop))
    laptop_old_prices.append(get_laptop_old_price(laptop))
    laptop_sale_type.append(get_laptop_sale_type(laptop))

all_laptops = merge_lists(laptop_links, laptop_names, laptop_prices, laptop_processor, laptop_ram, laptop_gpu, laptop_storage, laptop_old_prices, laptop_sale_type)
print(all_laptops)

with open("AcerHTML(103).json", "w") as f:
    json.dump(all_laptops, f, indent=4)

# laptop = all_laptop_info_html[0]
# print(laptop.find(class_='price'))
# print(remove_extra_stuff(laptop.find(class_='price').text))

# TODO make a function that tells how many 'N/A' I got

# prints(laptop_links)
# prints(laptop_names)
# prints(laptop_processor)
# prints(laptop_ram)
# prints(laptop_storage)
# prints(laptop_prices)

# print(len(laptop_links))
# print(len(laptop_names))
# print(len(laptop_processor))
# print(len(laptop_ram))
# print(len(laptop_storage))
# print(len(laptop_prices))

print("\n\nProcess finished --- %s seconds ---" % (time.time() - start_time))
