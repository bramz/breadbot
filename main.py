"""
BreadBot Launcher

This script serves as the entry point for launching BreadBot, a cryptocurrency trading bot.
It initializes the bot with required parameters and starts the trading process.

Usage:
1. Configure settings in config/settings.py, including INFURA_URL, WALLETS, and EXCHANGES.
2. Ensure that all necessary dependencies are installed.
3. Run this script to start BreadBot and begin trading.

Example:
    python main.py
"""

import logging
import requests
from typing import Dict, List, Union
from bot import BreadBot
from config.settings import GDATA, INFURA_URL, WALLETS, EXCHANGES
from util import market_analysis, risk_management, exchange_api

# Configure logger
logger = logging.getLogger(__name__)

def get_historical_data(api_endpoint: str, symbol: str) -> Union[Dict, None]:
    """
    Fetch historical data from a specified API endpoint.

    Args:
        api_endpoint (str): The URL of the API endpoint.
        symbol (str): The trading symbol.

    Returns:
        dict or None: Historical data as a dictionary if successful, None otherwise.
    """
    url = f"{api_endpoint}/us/trades?symbols={symbol}"
    params = {"limit": 1000, "sort": "asc"}
    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": API_KEY,
        "APCA-API-SECRET-KEY": API_BASE_URL
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        logger.info(f"Successfully fetched historical data for {symbol} from {api_endpoint}")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching historical data from {url}: {e}")
        return None
    
def adapt_historical_data(raw_data: Dict, symbol: str) -> List[Dict[str, Union[str, float]]]:
    """
    Adapts raw historical data to the expected format.

    Args:
        raw_data (dict): The raw data fetched from Alpaca.
        symbol (str): The symbol for which the data was fetched.

    Returns:
        List[Dict[str, Union[str, float]]]: Adapted data in the expected format.
    """
    adapted_data = []
    for item in raw_data.get("trades", []):
        adapted_data.append({
            "token": symbol,
            "price": item["p"]  # Assuming "p" is the price in the returned data
        })
    logger.info(f"Adapted historical data for {symbol}")
    return adapted_data
def main() -> None:
    """
    Main function to initialize BreadBot and start trading.

    Steps:
    1. Initialize BreadBot with settings from config/settings.py.
    2. Start trading using BreadBot.
    3. Retrieve historical data from supported APIs and perform backtesting.
    """
    logging.basicConfig(level=logging.INFO)  # Set logging level to INFO

    # Initialize trading strategy and risk management
    # moving_average_period = 20  # Example period for moving average, adjust as needed
    # trading_strategy = market_analysis.TrendingStrategy(moving_average_period)
    # risk_manager = risk_management.RSIAnalysis()
    # exchange_api_client = exchange_api.APIClient(API_BASE_URL, API_KEY)

    # Initialize BreadBot
    breadbot = BreadBot(
        INFURA_URL,
        WALLETS,
        EXCHANGES
        # trading_strategy,
        # risk_manager,
        # exchange_api_client
    )

    # Start trading
    breadbot.start_trading()
    
    # Get historical data from all supported APIs
    historical_data: List[Dict[str, Union[str, float]]] = []
    for exchange, api_details in EXCHANGES.items():
        if 'historical_data_endpoint' in api_details:
            for symbol in GDATA["symbols"]:
                encoded_symbol = symbol.replace('/', '%2F')  # URL encoding for the symbol
                raw_data = get_historical_data(api_details['historical_data_endpoint'], encoded_symbol)
                if raw_data:
                    adapted_data = adapt_historical_data(raw_data, symbol)
                    historical_data.extend(adapted_data)

    # Perform backtesting if historical data is available
    if historical_data:
        breadbot.backtest_strategy(historical_data)

if __name__ == "__main__":
    main()
