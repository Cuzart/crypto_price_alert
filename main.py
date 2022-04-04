from decouple import config as getenv
from functions import  get_trending_assets, check_price_action, send_telegram, send_email
from pycoingecko import CoinGeckoAPI
import time
import requests

watched_assets = getenv('WATCHED_ASSETS')
notifications = {}

counter = 0
seconds_in_day = 24 * 60 * 60
iterations_until_refresh = seconds_in_day / int(getenv('TIME_INTERVAL'))

while True:
    try:
        old_notifications = dict(notifications)
        check_price_action(watched_assets, notifications)

        # reset after 24h = after iteration_until_refresh
        counter += 1
        if counter % iterations_until_refresh == 0: notifications = {}
        print(counter)

        # only if there is a new notification added
        if any(x not in old_notifications for x in notifications):
          message = "New abnormal price actions! 📈 🥳\n\n"
          message += "🚨 Price Alerts 🚨 \n\n"
          for note in notifications:
            message += "Current price of {0[0]} is at {0[1]}€ with a {0[2]}% change in 24h.".format(notifications[note]) + '\n\n'

          # add assets that are trending right now
          message += get_trending_assets(watched_assets)

          # uncomment for sending email notifications
          # send_email("New abnormal price actions! 📈 🥳", message)
          send_telegram(message)

    except requests.exceptions.Timeout:
        print("Timeout occured")
    except requests.exceptions.ConnectionError:
        print("Connection Error occured")

    time.sleep(int(getenv('TIME_INTERVAL')))
