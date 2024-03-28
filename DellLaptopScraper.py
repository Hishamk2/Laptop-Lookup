from bs4 import BeautifulSoup
from itertools import cycle
import requests

# What do I want to do?
# Get name of laptop, price, link, RAM, Processor

print("Start of the program")

# TODO This link is for laptops sorted from low to high, shouldnt matter though

# URL = """
# https://www.dell.com/en-ca/search/laptop?sb=pricing.saleprice,asc&p=1&t=Product&r=37654
# """
URL = """
https://www.dell.com/en-ca/search/laptop?r=37654,37789&p=1&ac=facetselect&t=Product
"""

# proxy = '124.156.219.100:80'
# header = {
#     'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}


user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    # Add more user agents here
]

user_agent_cycle = cycle(user_agents)


headers = {
    "User-Agent": next(user_agent_cycle)
}
page = requests.get(URL, headers=headers)
page_html = page.text
# print(page.status_code)
print(page.status_code)
print(page.headers)

# Gets the response code
# page = requests.get(URL, proxies={'http': proxy, 'https': proxy}, timeout=3)
# page = requests.get(URL, headers=header, timeout=3)
# page_html = page.text  # Gets the HTML content of the page
# print(page.status_code)

# TODO Trees or smthn is going on here, LEARN MORE ABT THIS
# Parses the HTML content into a BeautifulSoup object
soup = BeautifulSoup(page_html, "html.parser")

# # Gets the range of what results qare beiung shown on the current page
# result_range = soup.find(class_="pageinfo")
# # Gets the number of results that are being shown on teh current page
# num_results_page = result_range.find_next("label").text[-1]

laptop_price = []
laptop_price_html = []
laptop_name_html = soup.findAll(class_="ps-dell-price ps-simplified")
count = 0
for price in laptop_name_html:
    if (count % 2 == 0):
        price_text = price.text.strip()
        laptop_price.append(price_text)
    count += 1

# TODO Look at what append does

laptop_name = []
laptop_name_html = []
laptop_name_html = soup.findAll(class_="ps-title")
for name in laptop_name_html:
    name_text = name.text
    laptop_name.append(name_text)
    print(name_text)


laptop_processor = []
laptop_processor_html = []
laptop_processor_html = soup.findAll(
    class_="ps-iconography-container ps-icon-specs-container")
for processor in laptop_processor_html:
    processor_text = processor.find(
        class_="ps-iconography-specs-label").text.strip()
    laptop_processor.append(processor_text)


laptop_ram = []
laptop_ram_html = []
laptop_ram_html = soup.findAll(
    class_="ps-iconography-container ps-icon-specs-container")
for ram in laptop_ram_html:
    ram_text = ram.findAll(
        class_="ps-iconography-specs-label")[-3].text.strip()
    laptop_ram.append(ram_text)

print(len(laptop_name_html))
print(len(laptop_price_html))
print(len(laptop_processor_html))
print(len(laptop_ram_html))

# for i in range(len(laptop_name_html)):
#     print(laptop_name[i], end="")
#     print(laptop_price[i])
#     print(laptop_processor[i])
#     print(laptop_ram[i])

# Try getting erht a tags instead

print("End of the program")

# "C:\Users\hamza\Documents\HISHAM\Computer Science\BestBuy Laptop Scraper"

# i3 https://www.dell.com/en-ca/search/laptop?r=37654&p=1&ac=facetselect&t=Product
# i5 https://www.dell.com/en-ca/search/laptop?r=37653&p=1&ac=facetselect&t=Product
