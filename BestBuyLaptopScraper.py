from bs4 import BeautifulSoup
import requests

print("Start of the program")


URL = "https://www.dell.com/en-ca/search/laptop?r=37654,37789&p=1&ac=facetselect&t=Product"
page = requests.get(URL)  # Gets the response code
page_html = page.text  # Gets the HTML content of the page

# TODO Trees or smthn is going on here, LEARN MORE ABT THIS
# TODO Could have also used filehandle: with open(URL) as f: soup = BS(f, 'html.parser')
# Parses the HTML content into a BeautifulSoup object
soup = BeautifulSoup(page_html, "html.parser")

# Doing soup.find("head") is same as doing soup.head
print(soup.find(class_="ps-dell-price ps-simplified").text)


print("End of the program")

# "C:\Users\hamza\Documents\HISHAM\Computer Science\BestBuy Laptop Scraper"

# i3 https://www.dell.com/en-ca/search/laptop?r=37654&p=1&ac=facetselect&t=Product
# i5 https://www.dell.com/en-ca/search/laptop?r=37653&p=1&ac=facetselect&t=Product
