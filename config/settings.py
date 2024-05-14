"""
settings.py - Configuration file for BreadBot
This file contains constants and settings used by BreadBot for various functionalities.

Usage:
- Update the INFURA_URL with your Infura project URL for Ethereum interactions.
- Fill in the PayPal credentials (PAYPAL_CLIENT_ID and PAYPAL_SECRET) for PayPal API integration. (Only if PayPal is needed)
- Add your wallet addresses and private keys in the WALLETS section for different cryptocurrencies.
- Configure exchange APIs and endpoints in the EXCHANGES section for trading functionalities.
"""

# Infura URL for Ethereum interactions
INFURA_URL = "https://holesky.infura.io/v3/infura_key_here"

# Values for PayPal credentials
PAYPAL_ENDPOINT = "https://api.paypal.com/v1/payments/payment"
PAYPAL_CLIENT_ID = "paypal_client_id"
PAYPAL_SECRET = "paypal_secret"

# Wallet credentials
WALLETS = {
    "binance": {
        "address": "binance_wallet_address",
        "private_key": "binance_private_key_placeholder",
    }
}

# Exchange APIs and endpoints
EXCHANGES = {
    # Values for Binance API
    "binance": {
        "balance_endpoint": "https://api.binance.us/api/v3/account",
        "price_endpoint": "https://api.binance.us/api/v3/ticker/price",
        "historical_data_endpoint": "https://api.binance.us/api/v3/klines?symbol=BTCUSDT&interval=1d",
        "api_key": "binance_api_key_placeholder",
        "api_secret": "binance_api_secret_placeholder",
        "api_module": "binance_api"
    },

    # Values for eToro API
    "etoro": {
        "balance_endpoint": "https://api.etoro.com/sapi/v1/account",
        "price_endpoint": "https://api.etoro.com/sapi/v1/marketdata/symbols",
        "historical_data_endpoint": "https://api.etoro.com/sapi/v1/marketdata/candles/daily",
        "api_module": "etoro_api"
    }
}

# Exception Handling
class SettingsException(Exception):
    """Exception raised for configuration errors in BreadBot settings."""

    def __init__(self, message="Invalid configuration in settings.py"):
        self.message = message
        super().__init__(self.message)

# Check for required settings
def validate_settings():
    """Validate settings in settings.py."""
    required_settings = ["INFURA_URL", "PAYPAL_CLIENT_ID", "PAYPAL_SECRET", "WALLETS", "EXCHANGES"]

    for setting in required_settings:
        if setting not in globals():
            raise SettingsException(f"{setting} is missing in settings.py")

# Run settings validation
validate_settings()
