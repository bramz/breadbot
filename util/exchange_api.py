"""
exchange_api.py - Module for handling exchange APIs and PayPal interactions

This module provides classes for interacting with various exchange APIs and conducting trades using PayPal.

Imports:
- requests: Library for making HTTP requests.

Classes:
- ExchangeAPI: Class for interacting with exchange APIs and conducting trades.
- APIClient: Class for making authenticated API requests to a base URL.
"""

import requests
from config.settings import PAYPAL_ENDPOINT, PAYPAL_CLIENT_ID, PAYPAL_SECRET

class ExchangeAPI:
    """
    Class for interacting with exchange APIs and conducting trades.

    Attributes:
    - api_key: API key for authentication.
    - api_secret: API secret for authentication.
    - exchanges: Dictionary containing exchange details.

    Methods:
    - buy(token, amount, price, exchange_name=None): Method for buying tokens on exchanges.
    - sell(token, amount, price, exchange_name=None): Method for selling tokens on exchanges.
    - _send_trade_request(token, amount, price, endpoint): Method for sending trade requests to exchanges.
    - _trade_with_paypal(amount): Method for conducting trades using PayPal.
    - _get_paypal_access_token(): Method for obtaining PayPal access token.
    - fetch_data(data_endpoint): Method for fetching data from APIs.
    """
    def __init__(self, api_key, api_secret, exchanges):
        self.api_key = api_key
        self.api_secret = api_secret
        self.exchanges = exchanges

    def buy(self, token, amount, price, exchange_name=None):
        """Method for buying tokens on exchanges."""
        for exchange_name, exchange in self.exchanges.items():
            if exchange_name != "paypal":
                response = self._send_trade_request(token, amount, price, exchange["buy_endpoint"])
                if response is not None:
                    return response
                elif token == "usd" and amount > 0 and exchange["buy_endpoint"] == PAYPAL_ENDPOINT:
                    paypal_order_id = self._trade_with_paypal(amount)
                    return paypal_order_id
        return None

    def sell(self, token, amount, price, exchange_name=None):
        """Method for selling tokens on exchanges."""
        for exchange_name, exchange in self.exchanges.items():
            if exchange_name != "paypal":
                response = self._send_trade_request(token, amount, price, exchange["sell_endpoint"])
                if response is not None:
                    return response
                elif token == "usd" and amount > 0 and exchange["sell_endpoint"] == PAYPAL_ENDPOINT:
                    paypal_order_id = self._trade_with_paypal(amount)
                    return paypal_order_id
        return None

    def send_trade_request(self, token, amount, price, endpoint):
        """Method for sending trade requests to exchanges."""
        try:
            headers = {"X-API-KEY": self.api_key, "X-API-SECRET": self.api_secret}
            data = {"token": token, "amount": amount, "price": price}
            response = requests.post(endpoint, headers=headers, data=data)
            if response.status_code == 200:
                return response.json()["order_id"]
            else:
                raise Exception(f"Error in trade request: {response.status_code} - {response.text}")
        except Exception as e:
            raise Exception(f"Error sending trade request: {str(e)}")

    def trade_with_paypal(self, amount):
        """Method for conducting trades using PayPal."""
        try:
            paypal_access_token = self._get_paypal_access_token()
            if paypal_access_token is not None:
                headers = {"Authorization": f"Bearer {paypal_access_token}"}
                data = {
                    "client_id": PAYPAL_CLIENT_ID,
                    "client_secret": PAYPAL_SECRET,
                    "amount": amount,
                    "currency": "USD",
                    "intent": "sale"
                }
                response = requests.post(PAYPAL_ENDPOINT, headers=headers, json=data)
                if response.status_code == 200:
                    return response.json()["order_id"]
                else:
                    raise Exception(f"Error trading with PayPal: {response.status_code} - {response.text}")
        except Exception as e:
            raise Exception(f"Error trading with PayPal: {str(e)}")

    def get_paypal_access_token(self):
        """Method for obtaining PayPal access token."""
        try:
            auth_url = "https://api.paypal.com/v1/oauth2/token"
            headers = {"Accept": "application/json", "Accept-Language": "en_US"}
            data = {
                "grant_type": "client_credentials",
                "client_id": PAYPAL_CLIENT_ID,
                "client_secret": PAYPAL_SECRET
            }
            response = requests.post(auth_url, headers=headers, data=data)
            if response.status_code == 200:
                return response.json()["access_token"]
            else:
                raise Exception(f"Error getting PayPal access token: {response.status_code} - {response.text}")
        except Exception as e:
            raise Exception(f"Error getting PayPal access token: {str(e)}")

    def fetch_data(self, data_endpoint):
        """Method for fetching data from APIs."""
        try:
            headers = {"X-API-KEY": self.api_key, "X-API-SECRET": self.api_secret}
            response = requests.get(data_endpoint, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error fetching data: {response.status_code} - {response.text}")
        except Exception as e:
            raise Exception(f"Error fetching data: {str(e)}")

class APIClient:
    """
    Class for making authenticated API requests to a base URL.

    Attributes:
    - base_url: Base URL for API requests.
    - api_key: API key for authentication.

    Methods:
    - get(endpoint): Method for making GET requests.
    - post(endpoint, data): Method for making POST requests.
    - put(endpoint, data): Method for making PUT requests.
    - delete(endpoint): Method for making DELETE requests.
    """
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def get(self, endpoint):
        """Method for making GET requests."""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(f"{self.base_url}/{endpoint}", headers=headers)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, data):
        """Method for making POST requests."""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(f"{self.base_url}/{endpoint}", headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint, data):
        """Method for making PUT requests."""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.put(f"{self.base_url}/{endpoint}", headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint):
        """Method for making DELETE requests."""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.delete(f"{self.base_url}/{endpoint}", headers=headers)
        response.raise_for_status()
        return response.json()
