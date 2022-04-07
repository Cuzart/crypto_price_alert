from threading import Thread
import time
from telegram_bot import TelegramBot, send_message
from decouple import config as getenv
from gecko import Gecko
import requests


def start_alert():
    gecko = Gecko()

    counter = 0
    seconds_in_day = 24 * 60 * 60
    iterations_until_refresh = seconds_in_day / int(getenv('TIME_INTERVAL'))

    while True:
        try:
            old_notifications = dict(gecko.notifications)
            gecko.check_price_action()

            # reset after 24h = after iterations_until_refresh
            counter += 1
            if counter % iterations_until_refresh == 0: gecko.notifications = {}
            print(counter)

            # only if there is a new notification added
            if any(x not in old_notifications for x in gecko.notifications):
                message = "New abnormal price actions! 📈 🥳\n\n"
                message += "🚨 Price Alerts 🚨 \n\n"
                for note in gecko.notifications:
                    message += "{0[0]} is at {0[1]}€ with a {0[2]}% change in 24h."\
                                 .format(gecko.notifications[note]) + '\n\n'

                # add assets that are trending right now
                message += gecko.get_trending_assets()

                # uncomment for sending email notifications
                # send_email("New abnormal price actions! 📈 🥳", message)
                send_message(message)

        except requests.exceptions.Timeout:
              print("Timeout occured")
        except requests.exceptions.ConnectionError:
              print("Connection Error occured")

        time.sleep(int(getenv('TIME_INTERVAL')))

alert_thread = Thread(target=start_alert)
alert_thread.start()
TelegramBot()



