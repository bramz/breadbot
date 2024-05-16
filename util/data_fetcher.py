"""
Data Fetcher

This module provides a class for fetching data from various sources using APIs.

To-Do:
- Implement more sophisticated error handling for API requests.
- Add support for handling different types of API responses, such as XML or CSV.
"""
import requests
import statistics
from typing import List, Dict, Union
from config import exchanges, PAYPAL_ENDPOINT, PAYPAL_CLIENT_ID, PAYPAL_SECRET
from exchange_api import ExchangeAPI

class DataFetcher:
    """
    A class for fetching data from various sources using APIs.

    Attributes:
        api_key (str): API key for authentication.
        api_secret (str): API secret for authentication.
        exchanges (dict): Dictionary of exchange data.
        exchange_api (ExchangeAPI): Instance of ExchangeAPI for interacting with exchanges.
    """
    def __init__(self, api_key: str, api_secret: str):
        """
        Initializes the DataFetcher with API key and secret.

        Args:
            api_key (str): API key for authentication.
            api_secret (str): API secret for authentication.
        """
        self.exchanges: Dict[str, Dict[str, str]] = exchanges
        self.exchange_api: ExchangeAPI = ExchangeAPI(api_key, api_secret, exchanges)

    def fetch_exchange_data(self, exchange_name: str) -> Union[Dict[str, str], None]:
        """
        Fetches data from a specific exchange.

        Args:
            exchange_name (str): Name of the exchange.

        Returns:
            dict or None: Exchange data if successful, None otherwise.
        """
        exchange = self.exchanges.get(exchange_name)
        if exchange:
            data_endpoint = exchange.get("data_endpoint")
            if data_endpoint:
                try:
                    response = requests.get(data_endpoint)
                    response.raise_for_status()  # Raise an exception for non-200 status codes
                    return response.json()
                except requests.RequestException as e:
                    print(f"Error fetching data from '{exchange_name}': {e}")
                    return None
            else:
                print(f"Data endpoint not found for exchange '{exchange_name}'.")
                return None
        else:
            print(f"Exchange '{exchange_name}' not found in config.")
            return None

    def fetch_exchange_prices(self, exchange_name: str, asset_name: str) -> List[float]:
        """
        Fetches asset prices from a specific exchange.

        Args:
            exchange_name (str): Name of the exchange.
            asset_name (str): Name of the asset.

        Returns:
            list: Asset prices if successful, empty list otherwise.
        """
        asset_prices = self.exchange_api.get_asset_prices(exchange_name, asset_name)
        if asset_prices:
            return asset_prices
        else:
            print(f"No prices found for '{asset_name}' on '{exchange_name}'.")
            return []

    # Other fetch methods with similar documentation and exception handling

    def calculate_correlation(self, asset1_prices: List[float], asset2_prices: List[float]) -> Union[float, None]:
        """
        Calculates the correlation between two sets of asset prices.

        Args:
            asset1_prices (list): Prices of asset 1.
            asset2_prices (list): Prices of asset 2.

        Returns:
            float or None: Correlation coefficient if successful, None otherwise.
        """
        if asset1_prices and asset2_prices:
            try:
                correlation = statistics.corrcoef(asset1_prices, asset2_prices)[0, 1]
                return correlation
            except Exception as e:
                print(f"Error calculating correlation: {e}")
                return None
        else:
            print("Error calculating correlation: Asset prices not provided.")
            return None
