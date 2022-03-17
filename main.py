from decouple import config as getenv
from functions import check_price_below, check_price_above, get_trending_assets, get_coingecko_id, check_price_action, send_email
from pycoingecko import CoinGeckoAPI

import time
import requests


cg = CoinGeckoAPI()

watched_assets = getenv('WATCHED_ASSETS')
notifications = {}

counter = 0
seconds_in_day = 24 * 60 * 60
iterations_until_refresh = seconds_in_day / int(getenv('TIME_INTERVAL'))

while True:
    try:
        count_notifications = len(notifications)
        check_price_action(watched_assets, notifications)

        # reset after 24h
        counter += 1
        print(counter)

        if counter % iterations_until_refresh == 0: notifications = {}

        # only if there is a new notification added
        if len(notifications) > count_notifications:
          message = "🚨 Price Alerts 🚨 \n\n"
          for note in notifications:
            message += notifications[note] + '\n\n'

          # add my assets that are trending right now
          message += get_trending_assets(watched_assets)
          send_email("New abnormal price actions! 📈 🥳 ", message)


    except requests.exceptions.Timeout:
        print("Timeout occured")
    except requests.exceptions.ConnectionError:
        print("Connection Error occured")

    time.sleep(int(getenv('TIME_INTERVAL')))
