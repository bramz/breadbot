"""
settings.py - Configuration file for BreadBot
This file contains constants and settings used by BreadBot for various functionalities.

Usage:
- Update the INFURA_URL with your Infura project URL for Ethereum interactions.
- Fill in the PayPal credentials (PAYPAL_CLIENT_ID and PAYPAL_SECRET) for PayPal API integration.
- Add your wallet addresses and private keys in the WALLETS section for different cryptocurrencies.
- Configure exchange APIs and endpoints in the EXCHANGES section for trading functionalities.

eToro API:
- eToro requires users to request API access. The following are some of the available APIs:
    - Discovery API: Allows discovery of customers in the eToro network who have opted-in for discovery.
    - Metadata API: Provides basic metadata for the eToro system, including reference tables for other endpoints.
    - System API: Provides general data on the full eToro System.
    - User API: Provides data on a user, including trading statistics.

Other Exchanges:
- Coinbase: Exchange for trading cryptocurrencies.
- Kraken: Cryptocurrency exchange platform.
- CoinGecko: Cryptocurrency market data aggregator.
- Robinhood: Commission-free trading platform.
- Gemini: Cryptocurrency exchange and custodian.
- MXC Global: Digital asset exchange platform.
- CoinStats: Cryptocurrency portfolio tracker.
- Bitstamp: Cryptocurrency exchange.
- Bitfinex: Cryptocurrency exchange platform.

Note: Replace placeholders with your actual API keys, secrets, wallet addresses, and Infura URL.
"""

# Infura URL for Ethereum interactions
INFURA_URL = "https://holesky.infura.io/v3/"

# Values for PayPal credentials
PAYPAL_ENDPOINT = "https://api.paypal.com/v1/payments/payment"
PAYPAL_CLIENT_ID = "your_paypal_client_id"
PAYPAL_SECRET = "your_paypal_secret"

# Wallet credentials
WALLETS = {
    "wallet1": {
        "address": "your_wallet1_address",
        "private_key": "your_wallet1_private_key",
    },
    # Other wallet configurations are commented out for simplicity.
    # Once there is a comprehensive understanding of the bot setup and usage,
    # additional support can be implemented for multiple wallets by removing comments and
    # configuring the necessary wallet settings.
    # "wallet2": {
    #     "address": "your_wallet2_address",
    #     "private_key": "your_wallet2_private_key",
    # },
}

# Exchange APIs and endpoints
EXCHANGES = {
    "binance": {
        "balance_endpoint": "https://api.binance.com/api/v3/account",
        "price_endpoint": "https://api.binance.com/api/v3/ticker/price",
        "historical_data_endpoint": "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d",
        "api_key": "YourBinanceApiKey",
        "api_secret": "YourBinanceApiSecret",
        "api_module": "binance_api"
    },
    # Other exchange configurations are commented out for simplicity.
    # Once there is a comprehensive understanding of the bot setup and usage,
    # additional support can be implemented for multiple exchanges by removing comments and
    # configuring the necessary exchange settings.
    # "etoro_real": {
    #     "balance_endpoint": "https://api.etoro.com/sapi/v1/account",
    #     "price_endpoint": "https://api.etoro.com/sapi/v1/marketdata/symbols",
    #     "historical_data_endpoint": "https://api.etoro.com/sapi/v1/marketdata/candles",
    #     "api_key": "YourEToroRealApiKey",
    #     "api_secret": "YourEToroRealApiSecret",
    #     "api_module": "etoro_api"
    # },
    # "etoro_virtual": {
    #     "balance_endpoint": "https://api.etoro.com/sapi/v1/account",
    #     "price_endpoint": "https://api.etoro.com/sapi/v1/marketdata/symbols",
    #     "historical_data_endpoint": "https://api.etoro.com/sapi/v1/marketdata/candles",
    #     "api_key": "YourEToroVirtualApiKey",
    #     "api_secret": "YourEToroVirtualApiSecret",
    #     "api_module": "etoro_api"
    # },
    # "coinbase": {
    #     "balance_endpoint": "https://api.coinbase.com/v2/accounts",
    #     "price_endpoint": "https://api.coinbase.com/v2/prices",
    #     "historical_data_endpoint": "https://api.coinbase.com/v2/prices/historical",
    #     "api_key": "YourCoinbaseApiKey",
    #     "api_secret": "YourCoinbaseApiSecret",
    #     "api_module": "coinbase_api"
    # },
    # "kraken": {
    #     "balance_endpoint": "https://api.kraken.com/0/private/Balance",
    #     "price_endpoint": "https://api.kraken.com/0/public/Ticker",
    #     "historical_data_endpoint": "https://api.kraken.com/0/public/OHLC",
    #     "api_key": "YourKrakenApiKey",
    #     "api_secret": "YourKrakenApiSecret",
    #     "api_module": "kraken_api"
    # },
    # "coingecko": {
    #     "price_endpoint": "https://api.coingecko.com/api/v3/simple/price",
    #     "historical_data_endpoint": "https://api.coingecko.com/api/v3/coins/bitcoin/history",
    #     "api_module": "coingecko_api"
    # },
    # "robinhood": {
    #     "balance_endpoint": "https://api.robinhood.com/accounts",
    #     "price_endpoint": "https://api.robinhood.com/quotes",
    #     "historical_data_endpoint": "https://api.robinhood.com/quotes/historical",
    #     "api_key": "YourRobinhoodApiKey",
    #     "api_secret": "YourRobinhoodApiSecret",
    #     "api_module": "robinhood_api"
    # },
    # "gemini": {
    #     "balance_endpoint": "https://api.gemini.com/v1/balances",
    #     "price_endpoint": "https://api.gemini.com/v1/pubticker",
    #     "historical_data_endpoint": "https://api.gemini.com/v1/trades",
    #     "api_key": "YourGeminiApiKey",
    #     "api_secret": "YourGeminiApiSecret",
    #     "api_module": "gemini_api"
    # },
    # "mxcglobal": {
    #     "balance_endpoint": "https://www.mxc.com/open/api/v2/account/info",
    #     "price_endpoint": "https://www.mxc.com/open/api/v2/market/ticker",
    #     "historical_data_endpoint": "https://www.mxc.com/open/api/v2/trades",
    #     "api_key": "YourMXCGlobalApiKey",
    #     "api_secret": "YourMXCGlobalApiSecret",
    #     "api_module": "mxcglobal_api"
    # },
    # "coinstats": {
    #     "balance_endpoint": "https://api.coinstats.app/public/v1/users/your_user_id/wallets",
    #     "price_endpoint": "https://api.coinstats.app/public/v1/coins",
    #     "historical_data_endpoint": "https://api.coinstats.app/public/v1/coins/bitcoin/history",
    #     "api_key": "YourCoinStatsApiKey",
    #     "api_secret": "YourCoinStatsApiSecret",
    #     "api_module": "coinstats_api"
    # },
    # "bitstamp": {
    #     "balance_endpoint": "https://www.bitstamp.net/api/v2/balance/",
    #     "price_endpoint": "https://www.bitstamp.net/api/v2/ticker/",
    #     "historical_data_endpoint": "https://www.bitstamp.net/api/v2/ohlc/",
    #     "api_key": "YourBitstampApiKey",
    #     "api_secret": "YourBitstampApiSecret",
    #     "api_module": "bitstamp_api"
    # },
    # "bitfinex": {
    #     "balance_endpoint": "https://api.bitfinex.com/v2/auth/r/wallets",
    #     "price_endpoint": "https://api.bitfinex.com/v2/tickers?symbols=tBTCUSD,tETHUSD,tUSDTUSD,tSOLUSD,tXMRUSD,tBCHUSD",
    #     "historical_data_endpoint": "https://api.bitfinex.com/v2/candles/trade:1D:tBTCUSD/hist",
    #     "api_key": "YourBitfinexApiKey",
    #     "api_secret": "YourBitfinexApiSecret",
    #     "api_module": "bitfinex_api"
    # }
}
