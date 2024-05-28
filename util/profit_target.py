import logging
from typing import List

logging.basicConfig(level=logging.INFO)

class ProfitTargetUtility:
    """
    Implements a profit target strategy for trading cryptocurrencies.

    Attributes:
        api_client (APIClient): Client for interacting with exchange APIs.
        target_profit (float): Target profit percentage to achieve.
        symbols (List[str]): List of symbols to trade.

    Methods:
        check_profit_target(symbol, current_price, entry_price): Checks if the profit target is reached.
        execute_trade(symbol, amount, current_price): Executes a trade if profit target is reached.
        run_strategy(): Runs the profit target strategy.
    """

    def __init__(self, api_client, target_profit: float, symbols: List[str]):
        self.api_client = api_client
        self.target_profit = target_profit
        self.symbols = symbols
        self.logger = logging.getLogger(__name__)

    def check_profit_target(self, symbol: str, current_price: float, entry_price: float) -> bool:
        """
        Checks if the profit target is reached.

        Args:
            symbol (str): The trading symbol.
            current_price (float): The current price of the symbol.
            entry_price (float): The entry price of the symbol.

        Returns:
            bool: True if the profit target is reached, False otherwise.
        """
        return current_price >= entry_price * (1 + self.target_profit / 100)

    def execute_trade(self, symbol: str, amount: float, current_price: float) -> None:
        """
        Executes a trade if profit target is reached.

        Args:
            symbol (str): The trading symbol.
            amount (float): The amount to trade.
            current_price (float): The current price of the symbol.
        """
        self.api_client.sell(symbol, amount, current_price)
        self.logger.info(f"Executed SELL for {symbol} at {current_price} reaching profit target.")

    def run_strategy(self) -> None:
        """
        Runs the profit target strategy.
        """
        for symbol in self.symbols:
            entry_price = self.api_client.get_entry_price(symbol)
            current_price = self.api_client.get_current_price(symbol)
            if self.check_profit_target(symbol, current_price, entry_price):
                amount_to_trade = self.api_client.get_position_size(symbol)
                self.execute_trade(symbol, amount_to_trade, current_price)
