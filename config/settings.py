"""
settings.py - Configuration file for BreadBot
This file contains constants and settings used by BreadBot for various functionalities.

Usage:
- Update the .env file with your actual API keys, secrets, wallet addresses, and Infura URL.
"""

import os
from dotenv import load_dotenv
from datetime import datetime

# Load settings from .env file
load_dotenv()

# Alpaca API Configuration
ALPACA_ACCOUNT_ID = os.getenv('ALPACA_ACCOUNT_ID')
ALPACA_API_KEY = os.getenv('ALPACA_API_KEY')
ALPACA_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
ALPACA_API_BASE_URL = os.getenv('ALPACA_API_BASE_URL')
ALPACA_MARKET_DATA_URL = os.getenv('ALPACA_MARKET_DATA_URL')
ALPACA_ACCOUNT_URL = os.getenv('ALPACA_ACCOUNT_URL')

# Infura URL for Ethereum interactions
INFURA_URL = os.getenv('INFURA_URL')

# PayPal credentials
PAYPAL_ENDPOINT = os.getenv('PAYPAL_ENDPOINT')
PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
PAYPAL_SECRET = os.getenv('PAYPAL_SECRET')

# General Data Configuration
current_year = datetime.now().year
today_date = datetime.now().strftime('%Y-%m-%d')

GDATA = {
    "symbols": os.getenv('GDATA_SYMBOLS').split(', '),
    "start_date": os.getenv('GDATA_START_DATE', f"{current_year}-01-01"),
    "end_date": os.getenv('GDATA_END_DATE', today_date),
}

# Wallet credentials
WALLETS = {
    "alpaca": {
        "address": os.getenv('ALPACA_ADDRESS'),
    },
}

# Exchange APIs and endpoints
EXCHANGES = {
    "alpaca": {
        "price_endpoint": f"{ALPACA_MARKET_DATA_URL}/v2/stocks/{GDATA['symbols'][0]}/last",
        "historical_data_endpoint": f"{ALPACA_MARKET_DATA_URL}/v1beta3/crypto",
        "api_url": f"{ALPACA_API_BASE_URL}/account",
        "api_key": ALPACA_API_KEY,
        "api_secret": ALPACA_SECRET_KEY,
        "api_module": "alpaca_api",
        "paper_trading": True
    },
}
