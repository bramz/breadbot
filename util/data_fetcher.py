"""
Data Fetcher

This module provides a class for fetching data from various sources using APIs.

To-Do:
- Implement more sophisticated error handling for API requests.
- Add support for handling different types of API responses, such as XML or CSV.
"""

import requests
import logging
import statistics
from typing import List, Dict, Union
from config import exchanges, PAYPAL_ENDPOINT, PAYPAL_CLIENT_ID, PAYPAL_SECRET
from exchange_api import ExchangeAPI

logging.basicConfig(level=logging.INFO)

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
        logging.info("DataFetcher initialized successfully.")

    def fetch_exchange_data(self, exchange_name: str) -> Union[Dict[str, str], None]:
        """
        Fetches data from a specific exchange.

        Args:
            exchange_name (str): Name of the exchange.

        Returns:
            dict or None: Exchange data if successful, None otherwise.
        """
        exchange = self.exchanges.get(exchange_name)
        if not exchange:
            logging.error(f"Exchange '{exchange_name}' not found in config.")
            return None

        data_endpoint = exchange.get("data_endpoint")
        if not data_endpoint:
            logging.error(f"Data endpoint not found for exchange '{exchange_name}'.")
            return None

        try:
            response = requests.get(data_endpoint)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Error fetching data from '{exchange_name}': {e}")
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
        try:
            asset_prices = self.exchange_api.get_asset_prices(exchange_name, asset_name)
            if asset_prices:
                return asset_prices
            else:
                logging.warning(f"No prices found for '{asset_name}' on '{exchange_name}'.")
                return []
        except Exception as e:
            logging.error(f"Error fetching prices for '{asset_name}' from '{exchange_name}': {e}")
            return []

    def calculate_correlation(self, asset1_prices: List[float], asset2_prices: List[float]) -> Union[float, None]:
        """
        Calculates the correlation between two sets of asset prices.

        Args:
            asset1_prices (list): Prices of asset 1.
            asset2_prices (list): Prices of asset 2.

        Returns:
            float or None: Correlation coefficient if successful, None otherwise.
        """
        if not asset1_prices or not asset2_prices:
            logging.error("Error calculating correlation: Asset prices not provided.")
            return None

        try:
            correlation = statistics.correlation(asset1_prices, asset2_prices)
            return correlation
        except Exception as e:
            logging.error(f"Error calculating correlation: {e}")
            return None
