import random
import time
import logging
import requests
from web3 import Web3
from util.exchange_api import APIClient
from util.risk_management import StopLoss, TrailingStop, PositionSizing, TrendAnalysis, VolatilityAnalysis, RSIAnalysis, ResistanceAnalysis, MovingAverage
from util.market_analysis import MarketAnalysisTools

class BreadBot:
    def __init__(self, infura_url, wallets, exchanges, trading_strategy, risk_manager, exchange_api):
        """
        Initialize BreadBot with necessary parameters.

        Parameters:
        - infura_url (str): URL for Infura API.
        - wallets (dict): Wallet information for different exchanges.
        - exchanges (dict): Exchange information with API keys, endpoints, etc.
        - trading_strategy (TradingStrategy): Object representing the trading strategy.
        - risk_manager (RiskManagement): Object handling risk management.
        - exchange_api (ExchangeAPI): API client for executing orders on exchanges.
        """
        self.web3 = Web3(Web3.HTTPProvider(infura_url))
        self.wallets = wallets
        self.exchanges = exchanges
        self.trading_strategy = trading_strategy
        self.risk_manager = risk_manager
        self.exchange_api = exchange_api
        self.logger = self.setup_logger()
        self.trend_analysis = TrendAnalysis()
        self.volatility_analysis = VolatilityAnalysis()
        self.rsi_analysis = RSIAnalysis()
        self.resistance_analysis = ResistanceAnalysis()
        self.market_analysis = MarketAnalysisTools()
        self.api_client = APIClient

    def setup_logger(self):
        """
        Set up logging configuration.

        Returns:
        - logger (logging.Logger): Configured logger object.
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler('crypto_bot.log')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def check_balance(self, token, exchange):
        """
        Check the balance of a token on an exchange.

        Parameters:
        - token (str): Token symbol to check balance.
        - exchange (str): Exchange name.

        Returns:
        - balance (float): Token balance on the exchange.
        """
        try:
            api_key = self.exchanges[exchange]["api_key"]
            api_secret = self.exchanges[exchange]["api_secret"]
            balance_endpoint = self.exchanges[exchange]["balance_endpoint"]
            headers = {"X-API-KEY": api_key, "X-API-SECRET": api_secret}
            response = requests.get(balance_endpoint, headers=headers)
            print(response.json())
            if response.status_code == 200:
                balance = response.json()["balance"]
                return balance[token]
            else:
                self.logger.error(f"Error fetching balance from {exchange}: {response.text}")
                return 0
        except requests.RequestException as e:
            self.logger.error(f"Error checking balance on {exchange}: {e}")
            self.logger.error(f"Response text: {response.text}")  # Print the response text
            return 0

    def get_token_price(self, token, exchange):
        """
        Get the current price of a token on an exchange.

        Parameters:
        - token (str): Token symbol to get price.
        - exchange (str): Exchange name.

        Returns:
        - price (float): Current price of the token.
        """
        try:
            price_endpoint = self.exchanges[exchange]["price_endpoint"]
            response = requests.get(price_endpoint)
            if response.status_code == 200:
                price = response.json()["price"]
                return price[token]
            else:
                self.logger.error(f"Error fetching price from {exchange}: {response.text}")
                return 0
        except requests.RequestException as e:
            self.logger.error(f"Error getting price on {exchange}: {e}")
            return 0

    def execute_trade(self, token, amount_to_trade, exchange):
        """
        Execute a trade for a token on an exchange.

        Parameters:
        - token (str): Token symbol to trade.
        - amount_to_trade (float): Amount of token to trade.
        - exchange (str): Exchange name.
        """
        try:
            current_price = self.get_token_price(token, exchange)
            trade_amount = min(amount_to_trade, self.check_balance(token, exchange))
            if trade_amount > 0:
                if current_price == 0:
                    self.logger.warning(f"{token} price is zero on {exchange}. Skipping trade.")
                    return

                # Buy logic
                if random.random() < 0.5 and self.should_buy(token, current_price):
                    buy_amount = trade_amount * random.uniform(0.1, 0.5)  # Random buy amount
                    self.logger.info(f"Buying {buy_amount} {token} on {exchange} at {current_price}")
                    self.execute_order("buy", token, buy_amount, current_price, exchange)

                # Sell logic
                if random.random() < 0.5 and self.should_sell(token, current_price):
                    sell_amount = trade_amount * random.uniform(0.1, 0.5)  # Random sell amount
                    self.logger.info(f"Selling {sell_amount} {token} on {exchange} at {current_price}")
                    self.execute_order("sell", token, sell_amount, current_price, exchange)
            else:
                self.logger.warning(f"Not enough balance to trade {token} on {exchange}.")
        except requests.RequestException as e:
            self.logger.error(f"Error executing trade on {exchange}: {e}")

    def execute_order(self, order_type, token, amount, price, exchange):
        """
        Execute a trading order on an exchange.

        Parameters:
        - order_type (str): Type of order (buy/sell).
        - token (str): Token symbol to trade.
        - amount (float): Amount of token to trade.
        - price (float): Price at which to execute the order.
        - exchange (str): Exchange name.
        """
        stop_loss_manager = StopLoss(self.risk_manager.stop_loss_ratio)
        trailing_stop_manager = TrailingStop(self.risk_manager.profit_take_ratio)
        position_sizing_manager = PositionSizing(0.01, 0.1)  # Example risk per trade and max drawdown

        trail_price = trailing_stop_manager.update_trailing_stop(price)
        trade_size = position_sizing_manager.calculate_trade_size(self.wallets[exchange], trail_price)

        order_id = self.exchange_api.execute_order(order_type, token, trade_size, price, exchange)
        self.logger.info(f"{order_type.capitalize()} order ID: {order_id}")

    def start_trading(self):
        """
        Start the trading process based on the defined strategy and parameters.
        """
        print("Exchanges available:", self.exchanges)  # Check if 'binance' is in the exchanges dictionary
        print("Wallets available:", self.wallets)      # Check the structure and content of self.wallets
        for token in ["eth", "btc", "usdt", "sol", "xmr", "bch"]:
            for exchange in self.exchanges:
                if exchange in self.wallets:
                    exchange_wallet = self.wallets[exchange]
                    if "balance" in exchange_wallet:
                        balance = exchange_wallet["balance"]
                        amount_to_trade = balance * 0.2  # Trade 20% of the balance
                        self.execute_trade(token, amount_to_trade, exchange)
                        time.sleep(5)  # Sleep for 5 seconds between trades
                    else:
                        print(f"No balance information found in wallet for exchange '{exchange}'.")
                else:
                    print(f"Wallet for exchange '{exchange}' not found.")
        # for token in ["eth", "btc", "usdt", "sol", "xmr", "bch"]:
        #     for exchange in self.exchanges:
        #         amount_to_trade = self.wallets[exchange] * 0.2  # Trade 20% of starting balance
        #         self.execute_trade(token, amount_to_trade, exchange)
        #         time.sleep(5)  # Sleep for 5 seconds between trades

    # def backtest_strategy(self, historical_data):
    #     """
    #     Backtest the trading strategy using historical data.

    #     Parameters:
    #     - historical_data (list): List of historical data points.
    #     """
    #     try:
    #         for data_point in historical_data:
    #             token = data_point["token"]
    #             price = data_point["price"]
    #             if self.should_buy(token, price):
    #                 self.logger.info(f"Backtesting: Buy {token} at {price}")
    #                 self.execute_trade(token, self.wallets["wallet1"] * 0.2, "wallet1")
    #             elif self.should_sell(token, price):
    #                 self.logger.info(f"Backtesting: Sell {token} at {price}")
    #                 self.execute_trade(token, self.wallets["wallet1"] * 0.2, "wallet1")
    #     except requests.RequestException as e:
    #         self.logger.error(f"Error in backtesting strategy: {e}")

    def backtest_strategy(self, historical_data):
        """
        Backtest the trading strategy using historical data.

        Parameters:
        - historical_data (list): List of dictionaries containing historical data points.
        """
        try:
            for data_point in historical_data:
                if isinstance(data_point, dict):  # Check if data_point is a dictionary
                    token = data_point.get("token")  # Use .get() method to safely get the value
                    price = data_point.get("price")
                    if token and price:  # Check if token and price are not None
                        if self.should_buy(token, price):
                            self.logger.info(f"Backtesting: Buy {token} at {price}")
                            self.execute_trade(token, self.wallets["wallet1"]["balance"] * 0.2, "wallet1")
                        elif self.should_sell(token, price):
                            self.logger.info(f"Backtesting: Sell {token} at {price}")
                            self.execute_trade(token, self.wallets["wallet1"]["balance"] * 0.2, "wallet1")
                    else:
                        self.logger.warning("Incomplete data point found in historical data.")
                else:
                    self.logger.warning("Invalid data format in historical data.")

        except requests.RequestException as e:
            self.logger.error(f"Error in backtesting strategy: {e}")

    def should_buy(self, token, current_price):
        """
        Determine if a buy signal should be generated based on the trading strategy.

        Parameters:
        - token (str): Token symbol to check for buy signal.
        - current_price (float): Current price of the token.

        Returns:
        - buy_signal (bool): True if a buy signal should be generated, False otherwise.
        """
        try:
            moving_average = self.market_analysis_tools.calculate_ema(self.get_token_prices(token), 50)

            if current_price > moving_average:
                if self.trend_analysis.is_above_moving_average(current_price, 100) and \
                        self.volatility_analysis.is_above_standard_deviation(current_price, moving_average, 10) and \
                        self.rsi_analysis.is_oversold(self.get_token_prices(token)) and \
                        self.resistance_analysis.calculate_resistance_level([100, 200, 150]) > 200:
                    return True  # Buy signal
            return False
        except (ValueError, KeyError) as e:
            self.logger.error(f"Error in should_buy for {token}: {e}")
            return False

    def should_sell(self, token, current_price):
        """
        Determine if a sell signal should be generated based on the trading strategy.

        Parameters:
        - token (str): Token symbol to check for sell signal.
        - current_price (float): Current price of the token.

        Returns:
        - sell_signal (bool): True if a sell signal should be generated, False otherwise.
        """
        try:
            moving_average = self.market_analysis_tools.calculate_ema(self.get_token_prices(token), 30)

            if current_price < moving_average:
                if self.trend_analysis.is_above_moving_average(current_price, moving_average) and \
                        self.volatility_analysis.is_above_standard_deviation(current_price, moving_average, 10) and \
                        not self.rsi_analysis.is_oversold(self.get_token_prices(token)) and \
                        self.resistance_analysis.calculate_resistance_level([100, 200, 150]) > 200:
                    return True  # Sell signal
            return False
        except (ValueError, KeyError) as e:
            self.logger.error(f"Error in should_sell for {token}: {e}")
            return False
