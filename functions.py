from decouple import config as getenv
from email.message import EmailMessage
from pycoingecko import CoinGeckoAPI
import smtplib
import os
import json


def send_email(subject, content):
    port = 465
    smtp_server = getenv("SMTP_SERVER")
    sender_email = getenv("SENDER_EMAIL")
    receiver_email = getenv("RECEIVER_EMAIL")
    password = getenv("SENDER_PW")

    server = smtplib.SMTP_SSL(smtp_server, port)

    server.ehlo()
    server.login(sender_email, password)

    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = subject
    msg['From'] = 'Price Alert Bot' + f' <{sender_email}>'
    msg['To'] = receiver_email

    server.send_message(msg)
    print("Server sent mail")


# check if trending asset is in asset list
def get_trending_assets(asset_list):
    cg = CoinGeckoAPI()
    top_7_trending = cg.get_search_trending()["coins"]
    trending = []
    my_trending_assets="⚡ Trending on Coingecko ⚡ \n\n"
    for coin in top_7_trending:
        trending.append(coin['item']['symbol'])
        if coin['item']['symbol'] in asset_list:
            my_trending_assets+= coin['item']['symbol'] + ', '

    # only if trending assets are in asset_list
    if any(x in asset_list for x in trending): 
      return my_trending_assets[:-2] 
    else:
      return ""

# check if price of assets in list are up/down by the limit in their 24h change
def check_price_action(asset_list, notifications):
    cg = CoinGeckoAPI()
    # call here to save on API request limit
    all_coins = cg.get_coins_list()
    for index, asset in enumerate(json.loads(asset_list)):
        asset_id = get_coingecko_id(asset, all_coins)
        asset_data = cg.get_price(ids=asset_id, vs_currencies='eur', include_24hr_change="true")

        asset_price = round(asset_data[asset_id]['eur'], 4)
        asset_24h_change = round(asset_data[asset_id]['eur_24h_change'], 2)
        
        # check for abnormal price activity on 24h change
        if asset_24h_change <  int(getenv("LOWER_LIMIT")) or asset_24h_change >  int(getenv("UPPER_LIMIT")):
          notifications[index] = (asset, asset_price, asset_24h_change)
          
    print(notifications)  


# returns the correct coingecko id of an asset by it's shortform e.g. bitcoin for BTC
def get_coingecko_id(asset_shortform, all_coins):
    for coin in all_coins:
        if coin['symbol'] == asset_shortform.lower():
            return coin['id']
    print("Sorry we found no match for your asset.")
