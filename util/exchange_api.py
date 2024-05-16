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
from typing import Dict, Union, Optional, List

from config.settings import PAYPAL_ENDPOINT, PAYPAL_CLIENT_ID, PAYPAL_SECRET

class ExchangeAPI:
    """
    Class for interacting with exchange APIs and conducting trades.

    Attributes:
    - api_key (str): API key for authentication.
    - api_secret (str): API secret for authentication.
    - exchanges (Dict[str, Dict[str, str]]): Dictionary containing exchange details.

    Methods:
    - buy(token: str, amount: float, price: float, exchange_name: Optional[str] = None) -> Union[str, None]:
        Method for buying tokens on exchanges.
    - sell(token: str, amount: float, price: float, exchange_name: Optional[str] = None) -> Union[str, None]:
        Method for selling tokens on exchanges.
    - send_trade_request(token: str, amount: float, price: float, endpoint: str) -> Union[str, None]:
        Method for sending trade requests to exchanges.
    - trade_with_paypal(amount: float) -> Union[str, None]:
        Method for conducting trades using PayPal.
    - get_paypal_access_token() -> Union[str, None]:
        Method for obtaining PayPal access token.
    - fetch_data(data_endpoint: str) -> Union[Dict, None]:
        Method for fetching data from APIs.
    """

    def __init__(self, api_key: str, api_secret: str, exchanges: Dict[str, Dict[str, str]]):
        self.api_key = api_key
        self.api_secret = api_secret
        self.exchanges = exchanges

    def buy(self, token: str, amount: float, price: float, exchange_name: Optional[str] = None) -> Union[str, None]:
        """Method for buying tokens on exchanges."""
        for exchange_name, exchange in self.exchanges.items():
            if exchange_name != "paypal":
                response = self.send_trade_request(token, amount, price, exchange["buy_endpoint"])
                if response is not None:
                    return response
                elif token == "usd" and amount > 0 and exchange["buy_endpoint"] == PAYPAL_ENDPOINT:
                    paypal_order_id = self.trade_with_paypal(amount)
                    return paypal_order_id
        return None

    def sell(self, token: str, amount: float, price: float, exchange_name: Optional[str] = None) -> Union[str, None]:
        """Method for selling tokens on exchanges."""
        for exchange_name, exchange in self.exchanges.items():
            if exchange_name != "paypal":
                response = self.send_trade_request(token, amount, price, exchange["sell_endpoint"])
                if response is not None:
                    return response
                elif token == "usd" and amount > 0 and exchange["sell_endpoint"] == PAYPAL_ENDPOINT:
                    paypal_order_id = self.trade_with_paypal(amount)
                    return paypal_order_id
        return None

    def send_trade_request(self, token: str, amount: float, price: float, endpoint: str) -> Union[str, None]:
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

    def trade_with_paypal(self, amount: float) -> Union[str, None]:
        """Method for conducting trades using PayPal."""
        try:
            paypal_access_token = self.get_paypal_access_token()
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

    def get_paypal_access_token(self) -> Union[str, None]:
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

    def fetch_data(self, data_endpoint: str) -> Union[Dict, None]:
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
    - base_url (str): Base URL for API requests.
    - api_key (str): API key for authentication.

    Methods:
    - get(endpoint: str) -> Dict:
        Method for making GET requests.
    - post(endpoint: str, data: Dict) -> Dict:
        Method for making POST requests.
    - put(endpoint: str, data: Dict) -> Dict:
        Method for making PUT requests.
    - delete(endpoint: str) -> Dict:
        Method for making DELETE requests.
    """
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def get(self, endpoint: str) -> Dict:
        """Method for making GET requests."""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(f"{self.base_url}/{endpoint}", headers=headers)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, data: Dict) -> Dict:
        """Method for making POST requests."""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(f"{self.base_url}/{endpoint}", headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint: str, data: Dict) -> Dict:
        """Method for making PUT requests."""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.put(f"{self.base_url}/{endpoint}", headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint: str) -> Dict:
        """Method for making DELETE requests."""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.delete(f"{self.base_url}/{endpoint}", headers=headers)
        response.raise_for_status()
        return response.json()
