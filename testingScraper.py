
import requests
from itertools import cycle

URL = """
https://www.dell.com/en-ca/search/laptop?r=37654,37789&p=1&ac=facetselect&t=Product
"""

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
response = requests.get(URL, headers=headers)
print(response.status_code)
print(response.headers)
