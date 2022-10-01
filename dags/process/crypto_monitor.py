import os
import json
import requests
from process.requests_session import requests_retry_session
from datetime import date
import pandas as pd


class CryptoMonitor:
    def __init__(self):
        self.url = "https://api.coingecko.com/api/v3/"
        self.session = requests_retry_session(session=requests.Session())
        self.similar_exchanges = self.extract_similar_markets()

    def extract_bitso_markets(self):
        bitso_url = self.url + "exchanges/bitso/tickers?include_exchange_logo=false&depth=false"
        bitso_response = self.session.get(bitso_url).json()
        bitso_markets = [f"{market['base']}/{market['target']}" for market in bitso_response["tickers"]]
        return bitso_markets


    def extract_exchanges(self):
        url = self.url + "exchanges/list"
        response = self.session.get(url).json()
        return [exchange["id"] for exchange in response]


    def extract_similar_markets(self):
        url = self.url + "exchanges/{id}/tickers?include_exchange_logo=false&depth=false"
        exchange_ids = self.extract_exchanges()
        bitso_markets = self.extract_bitso_markets()
        similar_exchanges = {}

        for id in exchange_ids:
            response = self.session.get(url.format(id=id))
            data = json.loads(response.content)
            if data:
                markets = [f"{market['base']}/{market['target']}" for market in data["tickers"]]
                idx = 0
                while idx < len(markets) - 1:
                    if markets[idx] in bitso_markets:
                        similar_exchanges[id] = markets
                        break
                    else:
                        idx += 1
        return similar_exchanges


    def create_exchanges_df(self):
        url = self.url + "https://api.coingecko.com/api/v3/exchanges?per_page=250&page={num_page}"
        exchanges_df = pd.DataFrame({"exchange_id": pd.Series(dtype="str"), "exchange_name": pd.Series(dtype="str"), "trust_score": pd.Series(dtype="int"), "trust_score_rank": pd.Series(dtype="int")})
        page = 1

        while True:
            response = self.session.get(url.format(num_page=page)).json()

            if not response:
                break

            df = pd.DataFrame(response)[["id", "name", "trust_score", "trust_score_rank"]]
            df.rename(columns={"id": "exchange_id", "name": "exchange_name"}, inplace=True)
            df[["trust_score", "trust_score_rank"]] = df[["trust_score", "trust_score_rank"]].astype('Int64')

            exchanges_df = pd.concat([exchanges_df, df], ignore_index=True)

            page += 1


        os.makedirs('data', exist_ok=True)
        exchanges_df = exchanges_df[exchanges_df.exchange_id.isin(self.similar_exchanges.keys())]

        exchanges_df.to_csv(f"data/exchanges.csv", index=False, sep=",", encoding="utf-8")


    def create_markets_df(self):
        filter_markets = []
        bitso_markets = self.extract_bitso_markets()

        for id, markets in self.similar_exchanges.items():
            row = {}
            for market in markets:
                if market in bitso_markets:
                    row["exchange_id"] = id
                    row["base"] = market.split("/")[0]
                    row["target"] = market.split("/")[1]
                    filter_markets.append(row)

        os.makedirs('data', exist_ok=True)    
        markets_df = pd.DataFrame(filter_markets)
        markets_df.to_csv(f"data/markets.csv", index=False, sep=",", encoding="utf-8")


    def create_rolling_volume_df(self):
        url = self.url + "exchanges/{id}/volume_chart?days=30"
        today = date.today().strftime("%Y-%m-%d")
        rolling_30_list = []

        for id in self.similar_exchanges.keys():
            response = self.session.get(url.format(id=id)).json()
            row = {}
            total_volume = 0
            for day in response:
                total_volume += float(day[1])
            row["exchange_id"] = id
            row["date"] = today
            row["volume_btc"] = total_volume/30
            rolling_30_list.append(row)

        os.makedirs('data', exist_ok=True)
        rolling_30_volume = pd.DataFrame(rolling_30_list)
        rolling_30_volume.to_csv(f"data/rolling_30_volume.csv", index=False, sep=",", encoding="utf-8")


def main():
    crypto_monitor = CryptoMonitor()
    crypto_monitor.create_exchanges_df()
    crypto_monitor.create_markets_df()
    crypto_monitor.create_rolling_volume_df()