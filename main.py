import requests
from bot import BreadBot
from config.settings import INFURA_URL, WALLETS, EXCHANGES
from util import market_analysis, risk_management, exchange_api

def get_historical_data(api_endpoint):
    try:
        response = requests.get(api_endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching historical data from {api_endpoint}: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error fetching historical data from {api_endpoint}: {str(e)}")
        return None

def main():
    breadbot = BreadBot(INFURA_URL, WALLETS, EXCHANGES, market_analysis.TrendingStrategy, risk_management.RSIAnalysis(), exchange_api.APIClient)
    breadbot.start_trading()

    # Get historical data from all supported APIs
    historical_data = {}
    for exchange, api_details in EXCHANGES.items():
        if 'historical_data_endpoint' in api_details:
            historical_data[exchange] = get_historical_data(api_details['historical_data_endpoint'])

    # Filter out None values (failed requests)
    historical_data = {k: v for k, v in historical_data.items() if v is not None}

    if historical_data:
        breadbot.backtest_strategy(historical_data)

if __name__ == "__main__":
    main()
