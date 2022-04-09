import requests
import json
from decouple import config as getenv
from gecko import Gecko
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters


class TelegramBot:
    def __init__(self):
        updater = Updater(getenv("TELEGRAM_API_TOKEN"), use_context=True)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler("help", self.help_command))
        dispatcher.add_handler(CommandHandler("start", self.start_command))
        dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), self.handle_message))
        updater.start_polling()
        updater.idle()

    # map messages to responses
    def get_response(self, text):
        user_message = str(text).lower()
        gecko = Gecko()

        if user_message in ("hello", "hi", "hey"):
            return "Hey! How's it going?"

        if user_message in ("assets", "my assets"):
            return gecko.asset_list

        # return top seven trending coins
        if user_message in ("limits"):
            return "Lower limit: {}%\nUpper limit: {}%".format(getenv("LOWER_LIMIT"), getenv("UPPER_LIMIT"))

        # return top seven trending coins
        if user_message in ("trending"):
            return "📈 Trending \n" + gecko.get_trending()

        # return top seven trending coins
        if user_message in ("interval", "time"):
            return "Prices are checked every {} minutes ⏰".format(int(getenv("TIME_INTERVAL")) // 60)

        if user_message in ("notifications", "state"):
            gecko.check_price_action()
            message = ""
            for line in gecko.notifications.values():
                message += "{0[0]}, {0[1]}€, {0[2]}% in 24h \n".format(line)
            
            if len(message) > 1: return message

        if user_message in ("global"):
            return gecko.get_global()

        # try to find a matching asset and return the price and 24h change
        if len(user_message) <= 5:
            for coin in gecko.all_coins:
                if coin['symbol'] == user_message.lower():
                    return "{0[0]} is at {0[1]}€ with a {0[2]}% change in 24h"\
                        .format(gecko.get_asset_data(user_message))
        return "unknown message"

    def start_command(self,  update: Update, context: CallbackContext):
        update.message.reply_text("Welcome!👋 \nTry '/help' to list all possbile commands or just wait to receive your alerts.")

    def help_command(self, update: Update, context: CallbackContext):
        response = ("Possible commands 🔧\n"
                    "/help - to list all commands\n" 
                    "'assets' - to list all watched assets\n"
                    "'trending' - for top seven trending coins on CoinGecko\n"
                    "'limits' - show limits for receiving an alert\n"
                    "'interval' - to show in which interval prices are checked\n"
                    "'state' - to show current state of watched prices\n"
                    "'global' - to list current stats of global crypto market\n"
                    "short form of an asset e.g. 'BTC' - for price information\n"
                    )
        update.message.reply_text(response)

    # handle incoming messages
    def handle_message(self, update: Update, context: CallbackContext):
        if isinstance(update.message.text, str):
            text = str(update.message.text).lower()
            response = self.get_response(text)
            update.message.reply_text(response)

# sending a message directly to the api
def send_message(message):
    url = "https://api.telegram.org/bot{}/sendMessage".format(getenv("TELEGRAM_API_TOKEN"))
    params = {"chat_id": getenv("TELEGRAM_CHAT_ID"), "text":message}
    message = requests.post(url=url, params=params)
    print("Telegram message sent", message)