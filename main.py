from decouple import config as getenv
from functions import check_price_below, check_price_above, check_is_trending, get_coingecko_id
from pycoingecko import CoinGeckoAPI

import time

cg = CoinGeckoAPI()

watched_assets = getenv('WATCHED_ASSETS')
price_goal_above = 0
price_goal_below = 0


asset_short = input("Enter shortform of the asset you want to watch: ")
asset_id = get_coingecko_id(asset_short)

in_above = input("Do you want to get notified when your asset is above your goal ? (y/n): ")
in_below = input("Do you want to get notified when your asset is below your goal ? (y/n): ")


if in_above == "y":
    price_goal_above = float(input("Enter your upper price goal: "))

if in_below == "y":
    price_goal_below = float(input("Enter your lower price goal: "))


while True:
    check_is_trending(watched_assets)

    # get the data from the api
    asset = cg.get_price(ids=asset_id, vs_currencies='eur', include_24hr_change="true", include_market_cap="true")

    asset_price = round(asset[asset_id]['eur'], 4)
    asset_24h_change = round(asset[asset_id]['eur_24h_change'], 2)
    asset_mcap = round(asset[asset_id]['eur_market_cap'])
    print("Current price of {} is at {}€ with a {}% change in 24h and a market cap of {:,}€."
          .format(asset_id, asset_price, asset_24h_change, asset_mcap))

    if in_above == "y":
        check_price_above(asset_price, price_goal_above, asset_short.upper())

    if in_below == "y":
        check_price_below(asset_price, price_goal_below, asset_short.upper())

    time.sleep(int(getenv('TIME_INTERVAL')))
