import requests
from bs4 import BeautifulSoup

def scrape_product(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    text = soup.get_text()

    return text[:5000]