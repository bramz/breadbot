import requests
from config.settings import PAYPAL_ENDPOINT, PAYPAL_CLIENT_ID, PAYPAL_SECRET

class ExchangeAPI:
    def __init__(self, api_key, api_secret, exchanges):
        self.api_key = api_key
        self.api_secret = api_secret
        self.exchanges = exchanges

    def buy(self, token, amount, price, exchange_name=None):
        for exchange_name, exchange in self.exchanges.items():
            if exchange_name != "paypal":
                response = self.send_trade_request(token, amount, price, exchange["buy_endpoint"])
                if response is not None:
                    return response
                elif token == "usd" and amount > 0 and exchange["buy_endpoint"] == PAYPAL_ENDPOINT:  # PayPal trade for USD
                    paypal_order_id = self.trade_with_paypal(amount)
                    return paypal_order_id
        return None

    def sell(self, token, amount, price, exchange_name=None):
        for exchange_name, exchange in self.exchanges.items():
            if exchange_name != "paypal":
                response = self.send_trade_request(token, amount, price, exchange["sell_endpoint"])
                if response is not None:
                    return response
                elif token == "usd" and amount > 0 and exchange["sell_endpoint"] == PAYPAL_ENDPOINT:  # PayPal trade for USD
                    paypal_order_id = self.trade_with_paypal(amount)
                    return paypal_order_id
        return None

    def send_trade_request(self, token, amount, price, endpoint):
        try:
            headers = {"X-API-KEY": self.api_key, "X-API-SECRET": self.api_secret}
            data = {"token": token, "amount": amount, "price": price}
            response = requests.post(endpoint, headers=headers, data=data)
            if response.status_code == 200:
                return response.json()["order_id"]
            else:
                print(f"Error in trade request: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error sending trade request: {str(e)}")
            return None

    def trade_with_paypal(self, amount):
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
                    print(f"Error trading with PayPal: {response.status_code} - {response.text}")
                    return None
        except Exception as e:
            print(f"Error trading with PayPal: {str(e)}")
            return None

    def get_paypal_access_token(self):
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
                access_token = response.json()["access_token"]
                return access_token
            else:
                print(f"Error getting PayPal access token: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error getting PayPal access token: {str(e)}")
            return None

    def fetch_data(self, data_endpoint):
        try:
            headers = {"X-API-KEY": self.api_key, "X-API-SECRET": self.api_secret}
            response = requests.get(data_endpoint, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching data: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error fetching data: {str(e)}")
            return None
        
class APIClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def get(self, endpoint):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(f"{self.base_url}/{endpoint}", headers=headers)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, data):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(f"{self.base_url}/{endpoint}", headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint, data):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.put(f"{self.base_url}/{endpoint}", headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.delete(f"{self.base_url}/{endpoint}", headers=headers)
        response.raise_for_status()
        return response.json()
