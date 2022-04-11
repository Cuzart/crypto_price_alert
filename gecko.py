from decouple import config as getenv
from pycoingecko import CoinGeckoAPI
import logging
import json


class Gecko:
    def __init__(self):
        self.asset_list = getenv("WATCHED_ASSETS")
        self.cg = CoinGeckoAPI()
        self.all_coins = self.cg.get_coins_list()
        self.notifications = {}

    # check if trending asset is in asset list
    def get_trending_assets(self):
        header = "⚡ Trending on Coingecko ⚡ \n\n"
        trending = []

        for coin in self.cg.get_search_trending()["coins"]:
            if coin['item']['symbol'] in self.asset_list:
                trending.append(coin['item']['symbol'])

        # only if trending assets are in asset_list
        return header + ", ".join(trending) if trending else ""

    # get list of trending coins
    def get_trending(self):
        trending = []
        for entry in self.cg.get_search_trending()["coins"]:
            data = entry['item']
            trending.append(f"{data['name']} ({data['symbol']})")
        return "\n".join(trending).rstrip("\n")

    # check if price of assets in list are up/down by the limit in their 24h change
    def check_price_action(self):
        for index, asset in enumerate(json.loads(self.asset_list)):
            try:
                asset_data = self.get_asset_data(asset)
            except:
              logging.info("Could not found data for asset " + asset.upper())

            asset_price = asset_data[1]
            asset_24h_change = asset_data[2]

            # check for abnormal price activity on 24h change
            if asset_24h_change < int(getenv("LOWER_LIMIT")) or asset_24h_change > int(getenv("UPPER_LIMIT")):
                self.notifications[index] = (asset, asset_price, asset_24h_change)
            else:
                # delete entry if it falls below/above the limit
                if index in self.notifications:
                    del self.notifications[index]

    # get asset with price and 24h change from api
    def get_asset_data(self, asset_shortform):
        asset_id = self.get_coingecko_id(asset_shortform)
        data = self.cg.get_price(ids=asset_id, vs_currencies='eur', include_24hr_change="true")
        
        asset_price = round(data[asset_id]['eur'], 4)
        asset_24h_change = round(data[asset_id]['eur_24h_change'], 2)

        return (asset_shortform.upper(), asset_price, asset_24h_change)

    # returns the correct coingecko id of an asset by it's shortform e.g. bitcoin for BTC
    def get_coingecko_id(self, asset_shortform):
        for coin in self.all_coins:
            if coin['symbol'] == asset_shortform.lower():
                return coin['id']

    def get_global(self):
        data = self.cg.get_global()
        global_mcap_change = round(data['market_cap_change_percentage_24h_usd'],2)
        btc_dominance = round(data['market_cap_percentage']['btc'],2)
        eth_dominance = round(data['market_cap_percentage']['eth'],2)

        return (f"Global stats 🌐\n"
                f"Market 24h change: {global_mcap_change}%\n"
                f"BTC dominance: {btc_dominance}%\n"
                f"ETH dominance: {eth_dominance}%" 
                )
