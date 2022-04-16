from bs4 import BeautifulSoup
import requests

headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15'}

def get_earn_offers():
    offers = []
    url = "https://www.coinbase.com/de/earn"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    card_container = soup.find("div", class_="EarnCards__CampaignCards-sc-1xftmgx-0")

    for e in card_container:
      offers.append(e.find("h3").text)

    return offers

    
def get_fng_index():
    url = "https://alternative.me/crypto/fear-and-greed-index/"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    index_now = soup.find("div", class_="fng-value")

    return index_now.find("div", "fng-circle").text

    
def get_rainbow_chart_state():
    url = "https://www.blockchaincenter.net/en/bitcoin-rainbow-chart/"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    state = soup.find("div", class_="legend").find("span", class_="active").text

    return state