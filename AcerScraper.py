import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import random
import time
import json
import time

start_time = time.time()

with open("AcerHTML(103).html", encoding='utf-8') as fp:
    soup = BeautifulSoup(fp, 'html.parser')

laptop_names = []
laptop_links = []
laptop_prices = []
laptop_processor = []
laptop_ram = []
laptop_storage = []

all_laptop_info_html = soup.findAll(class_="item product product-item")

    
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

for laptop in all_laptop_info_html:
    laptop_name = laptop.find(class_="product name product-item-name")
    laptop_names.append(laptop_name.text.strip())
    laptop_links.append(laptop_name.find(class_='product-item-link').get('href'))
    laptop_processor.append(get_laptop_processor(laptop))
    laptop_ram.append(get_laptop_ram(laptop))

laptop = all_laptop_info_html[0]
laptop_info = laptop.find(class_='clearfix').text.strip().split('\n')
print('laptop_info',laptop_info)
laptop_info_lower = convert_to_lowercase(laptop_info)
print('laptop_info',laptop_info)
print('laptop_info_lower',laptop_info_lower)
print(find_laptop_processor_index(laptop_info_lower))


prints(laptop_links)
prints(laptop_names)
prints(laptop_processor)
prints(laptop_ram)
# prints(laptop_storage)
# prints(laptop_prices)

# print(len(laptop_links))
# print(len(laptop_names))
# print(len(laptop_processor))
print(len(laptop_ram))

print(time.time())
print("\n\nProcess finished --- %s seconds ---" % (time.time() - start_time))
