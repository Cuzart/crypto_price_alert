from threading import Thread
import logging
import time
from telegram_bot import TelegramBot, send_message
from decouple import config as getenv
from gecko import Gecko
import requests


def start_alert():
    logging.basicConfig(level=logging.INFO)
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
            if counter % iterations_until_refresh == 0:
              logging.info(f'Notifications refreshed after: {counter} iterations')
              gecko.notifications = {}

            logging.info(f"Iteration: {counter} with {gecko.notifications}")

            # only if there is a new notification added
            if any(x not in old_notifications for x in gecko.notifications):
                notifications_sorted = sorted(gecko.notifications.values(), key=lambda tupl: tupl[2], reverse=True)
                message = "New abnormal price actions! 🥳\n\n"
                message += "Price Alerts 🚨 \n\n"

                for entry in notifications_sorted:
                    color =  "🟢" if entry[2] > 0 else "🔴"
                    message += color +  " {0[0]} is at {0[1]}€ with a {0[2]}% change in 24h."\
                                 .format(entry) + '\n\n'

                # add assets that are trending right now
                message += gecko.get_trending_assets()

                # uncomment for sending email notifications
                # send_email("New abnormal price actions! 📈 🥳", message)
                send_message(message)

        except requests.exceptions.Timeout:
              logging.error("Timeout occured")
        except requests.exceptions.ConnectionError:
              logging.error("Connection Error occured")

        time.sleep(int(getenv('TIME_INTERVAL')))

alert_thread = Thread(target=start_alert)
alert_thread.start()
TelegramBot()



