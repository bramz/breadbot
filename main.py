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
from typing import Dict, Union
from bot import BreadBot
from config.settings import INFURA_URL, WALLETS, EXCHANGES
from util import market_analysis, risk_management, exchange_api

logger = logging.getLogger(__name__)

def get_historical_data(api_endpoint: str) -> Union[Dict, None]:
    """
    Fetch historical data from a specified API endpoint.

    Args:
        api_endpoint (str): The URL of the API endpoint.

    Returns:
        dict or None: Historical data as a dictionary if successful, None otherwise.
    """
    try:
        with requests.get(api_endpoint) as response:
            response.raise_for_status()
            return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching historical data from {api_endpoint}: {e}")
        return None

def main() -> None:
    """
    Main function to initialize BreadBot and start trading.

    Steps:
    1. Initialize BreadBot with settings from config/settings.py.
    2. Start trading using BreadBot.
    3. Retrieve historical data from supported APIs and perform backtesting.
    """
    logging.basicConfig(level=logging.INFO)  # Set logging level to INFO

    breadbot = BreadBot(INFURA_URL, WALLETS, EXCHANGES, market_analysis.TrendingStrategy, risk_management.RSIAnalysis(), exchange_api.APIClient)
    breadbot.start_trading()

    # Get historical data from all supported APIs
    historical_data: Dict[str, Dict[str, Union[str, int, float]]] = {}
    for exchange, api_details in EXCHANGES.items():
        if 'historical_data_endpoint' in api_details:
            historical_data[exchange] = get_historical_data(api_details['historical_data_endpoint'])

    # Filter out None values (failed requests)
    historical_data = {k: v for k, v in historical_data.items() if v is not None}

    if historical_data:
        breadbot.backtest_strategy(historical_data)

if __name__ == "__main__":
    main()