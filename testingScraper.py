
import requests
from itertools import cycle
import random
from urllib.parse import urlparse


URL = """
https://www.scrapethissite.com/pages/forms/
"""

user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
               "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
               "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/124.0.6367.88 Mobile/15E148 Safari/604.1",
               "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/124.0.6367.88 Mobile/15E148 Safari/604.1",
               "Mozilla/5.0 (iPod; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/124.0.6367.88 Mobile/15E148 Safari/604.1",
               "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.82 Mobile Safari/537.36"]

user_agent_cycle = cycle(user_agents)

parameters = {
    'api_key': '335f5cac-8af6-4009-98e8-0f532937487b',
    'url': URL
}

# headers = {
#     "Referer": "https://www.dell.com/en-ca/search/laptop?r=37654,37789&p=1&ac=facetselect&t=Product",
#     "Sec-Ch-Ua": '''"hromium;v="124", "Google Chrome";v="124", "Not-A.Brand";v="99" ''',
#     "Sec-Ch-Ua-Mobile": "?0",
#     "Sec-Ch-Ua-Platform": "Windows",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
#     "X-Amzn-Trace-Id": "Root=1-6410831d-666f197b78c8e97a3013bea9"
# }

# REMEMBER TO CHANGE THE PATH TO WHATEVER THE LINK IS


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


URL = 'https://www.dell.com/en-ca/search/laptop?r=37654,37789&p=1&ac=facetselect&t=Product'
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


# response = requests.get(URL, headers=headers)
# print(response.status_code)
# print(response.headers)

response = requests.get("http://httpbin.org/headers",
                        headers=headers[random.randint(0, len(headers) - 1)])
print(response.status_code)
print(response.headers)
print(response.text)

# response = requests.get(
#     "https://www.dell.com/en-ca/search/laptop?r=37654,37789&p=1&ac=facetselect&t=Product", headers=headers)
# print(response.status_code)
# print(response.headers)
