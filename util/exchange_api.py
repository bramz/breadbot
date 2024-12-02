"""
exchange_api.py - Module for handling exchange APIs and PayPal interactions

This module provides classes for interacting with various exchange APIs and conducting trades using PayPal.
"""

import requests
import logging
from typing import Dict, Union, Optional

class ExchangeAPI:
    """
    Class for interacting with exchange APIs and conducting trades.

    Attributes:
    - base_url (str): Base URL for the exchange API.
    - api_key (str): API key for authentication.
    - api_secret (str): API secret for authentication.

    Methods:
    - buy(token: str, amount: float, price: float) -> Union[str, None]:
        Method for buying tokens on exchanges.
    - sell(token: str, amount: float, price: float) -> Union[str, None]:
        Method for selling tokens on exchanges.
    - send_trade_request(token: str, amount: float, price: float, endpoint: str) -> Union[str, None]:
        Method for sending trade requests to exchanges.
    - fetch_data(data_endpoint: str) -> Union[Dict, None]:
        Method for fetching data from APIs.
    """

    def __init__(self, base_url: str, api_key: str, api_secret: str):
        self.base_url = base_url
        self.api_key = api_key
        self.api_secret = api_secret
        self.logger = logging.getLogger(__name__)

    def buy(self, token: str, amount: float, price: float) -> Union[str, None]:
        """Method for buying tokens on exchanges."""
        try:
            response = self.send_trade_request(token, amount, price, f"{self.base_url}/buy")
            return response
        except Exception as e:
            self.logger.error(f"Error in buy method: {e}")
            return None

    def sell(self, token: str, amount: float, price: float) -> Union[str, None]:
        """Method for selling tokens on exchanges."""
        try:
            response = self.send_trade_request(token, amount, price, f"{self.base_url}/sell")
            return response
        except Exception as e:
            self.logger.error(f"Error in sell method: {e}")
            return None

    def send_trade_request(self, token: str, amount: float, price: float, endpoint: str) -> Union[str, None]:
        """Method for sending trade requests to exchanges."""
        try:
            headers = {"X-API-KEY": self.api_key, "X-API-SECRET": self.api_secret}
            data = {"token": token, "amount": amount, "price": price}
            response = requests.post(endpoint, headers=headers, json=data)
            response.raise_for_status()
            return response.json().get("order_id")
        except requests.RequestException as e:
            self.logger.error(f"Error sending trade request: {e}")
            return None

    def fetch_data(self, data_endpoint: str) -> Union[Dict, None]:
        """Method for fetching data from APIs."""
        try:
            headers = {"X-API-KEY": self.api_key, "X-API-SECRET": self.api_secret}
            response = requests.get(data_endpoint, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Error fetching data: {e}")
            return None

class APIClient:
    """
    Class for making authenticated API requests to a base URL.

    Attributes:
    - base_url (str): Base URL for API requests.
    - api_key (str): API key for authentication.
    """

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.logger = logging.getLogger(__name__)

    def _get_headers(self) -> Dict[str, str]:
        """Generate headers for API requests."""
        return {"Authorization": f"Bearer {self.api_key}"}

    def get(self, endpoint: str) -> Dict:
        """Method for making GET requests."""
        try:
            response = requests.get(f"{self.base_url}/{endpoint}", headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Error making GET request: {e}")
            return {}

    def post(self, endpoint: str, data: Dict) -> Dict:
        """Method for making POST requests."""
        try:
            response = requests.post(f"{self.base_url}/{endpoint}", headers=self._get_headers(), json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Error making POST request: {e}")
            return {}

    def put(self, endpoint: str, data: Dict) -> Dict:
        """Method for making PUT requests."""
        try:
            response = requests.put(f"{self.base_url}/{endpoint}", headers=self._get_headers(), json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Error making PUT request: {e}")
            return {}

    def delete(self, endpoint: str) -> Dict:
        """Method for making DELETE requests."""
        try:
            response = requests.delete(f"{self.base_url}/{endpoint}", headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Error making DELETE request: {e}")
            return {}

class AlpacaAPI:
    """
    Class for interacting with the Alpaca API.

    Attributes:
    - base_url (str): Base URL for Alpaca API.
    - market_data_url (str): URL for Alpaca market data.
    - headers (Dict[str, str]): Headers for API requests.
    """

    def __init__(self, config: Dict[str, str]):
        self.base_url = config.get('base_url')
        self.market_data_url = config.get('market_data_url')
        self.headers = {
            'APCA-API-KEY-ID': config.get('api_key'),
            'APCA-API-SECRET-KEY': config.get('api_secret')
        }
        self.logger = logging.getLogger(__name__)

    def get_account(self) -> Dict:
        """Get account information from Alpaca API."""
        try:
            response = requests.get(f"{self.base_url}/v2/account", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Error getting account: {e}")
            return {}

    def get_current_price(self, symbol: str) -> Dict:
        """Get the current price of a symbol from Alpaca API."""
        try:
            response = requests.get(f"{self.market_data_url}/v2/stocks/{symbol}/last", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Error getting current price: {e}")
            return {}

    def get_historical_data(self, symbol: str, start: str, end: str, timeframe: str = '1D') -> Dict:
        """Get historical data for a symbol from Alpaca API."""
        try:
            params = {
                'symbols': symbol,
                'start': start,
                'end': end,
                'timeframe': timeframe
            }
            response = requests.get(f"{self.market_data_url}/v1beta3/crypto/us/bars", headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Error getting historical data: {e}")
            return {}