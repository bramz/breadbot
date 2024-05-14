import requests
import statistics
from config import exchanges, PAYPAL_ENDPOINT, PAYPAL_CLIENT_ID, PAYPAL_SECRET
from exchange_api import ExchangeAPI

class DataFetcher:
    def __init__(self, api_key, api_secret):
        self.exchanges = exchanges
        self.exchange_api = ExchangeAPI(api_key, api_secret, exchanges)

    def fetch_exchange_data(self, exchange_name):
        exchange = self.exchanges.get(exchange_name)
        if exchange:
            data_endpoint = exchange.get("data_endpoint")
            if data_endpoint:
                response = requests.get(data_endpoint)
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"Error fetching data from '{exchange_name}': {response.status_code} - {response.text}")
                    return None
            else:
                print(f"Data endpoint not found for exchange '{exchange_name}'.")
                return None
        else:
            print(f"Exchange '{exchange_name}' not found in config.")
            return None

    def fetch_exchange_prices(self, exchange_name, asset_name):
        asset_prices = self.exchange_api.get_asset_prices(exchange_name, asset_name)
        if asset_prices:
            return asset_prices
        else:
            print(f"No prices found for '{asset_name}' on '{exchange_name}'.")
            return []

    def fetch_news_data(self, source):
        news_url = f"https://newsapi.org/v2/everything?q={source}&apiKey=YOUR_NEWS_API_KEY"
        response = requests.get(news_url)
        if response.status_code == 200:
            return response.json().get("articles", [])
        else:
            print(f"Error fetching news data from '{source}': {response.status_code} - {response.text}")
            return []

    def fetch_volume_data(self, exchange_name):
        volume_data = self.exchange_api.get_volume_data(exchange_name)
        if volume_data:
            return volume_data
        else:
            print(f"No volume data found for '{exchange_name}'.")
            return []

    def fetch_event_data(self, event_id):
        event_url = f"https://example.com/events/{event_id}"
        response = requests.get(event_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching event data for event '{event_id}': {response.status_code} - {response.text}")
            return {}

    def calculate_correlation(self, asset1_prices, asset2_prices):
        if asset1_prices and asset2_prices:
            correlation = statistics.corrcoef(asset1_prices, asset2_prices)[0, 1]
            return correlation
        else:
            print("Error calculating correlation: Asset prices not provided.")
            return None
