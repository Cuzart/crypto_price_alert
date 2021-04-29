from decouple import config as getenv
from email.message import EmailMessage
from pycoingecko import CoinGeckoAPI
import smtplib
import os


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
    msg['From'] = sender_email
    msg['To'] = receiver_email

    server.send_message(msg)
    print("Server sent mail")


# send mail if price is below your goal
def check_price_below(price, goal, asset_shortform):
    if price <= goal:
        difference = round(goal - price, 4)
        send_email("New lower price goal for {}! 📈 🥳".format(asset_shortform),
                   "{} is currently {}€ under your goal of {}€.\n\n The current price is at {}€."
                   .format(asset_shortform, difference, goal, round(price, 4)))


# send mail if price is above your goal
def check_price_above(price, goal, asset_shortform):
    if price >= goal:
        difference = round(price - goal, 4)
        send_email("New upper price goal for {}! 📉 🥳".format(asset_shortform),
                   "{} is currently {}€ above your goal of {}€.\n\n The current price is at {}€."
                   .format(asset_shortform.upper(), difference, goal, round(price, 4)))


# check if trending asset is in asset list
def check_is_trending(asset_list):
    cg = CoinGeckoAPI()
    top_7_trending = cg.get_search_trending()["coins"]
    trending = []
    for coin in top_7_trending:
        trending.append(coin['item']['symbol'])
        if coin['item']['symbol'] in asset_list:
            price = cg.get_price(ids=coin['item']['id'], vs_currencies='eur')[coin['item']['id']]['eur']
            print("-" * 50 + "TRENDING" + "-" * 50)
            print("{} is trending now at {}€️".format(coin['item']['symbol'], round(price, 4)))
            print("-" * 108)


# returns the correct coingecko id of an asset by it's shortform e.g. BTC
def get_coingecko_id(asset_shortform):
    cg = CoinGeckoAPI()
    all_coins = cg.get_coins_list()
    for coin in all_coins:
        if coin['symbol'] == asset_shortform.lower():
            return coin['id']

    print("Sorry we found no match for your asset.")


# triggers a desktop notification
def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))
