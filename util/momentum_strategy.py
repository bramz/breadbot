import pandas as pd
import numpy as np
from typing import List
import logging

logging.basicConfig(level=logging.INFO)

class MomentumStrategyUtility:
    """
    Implements a momentum trading strategy for cryptocurrencies.

    Attributes:
        api_client (APIClient): Client for interacting with exchange APIs.
        symbols (List[str]): List of symbols to trade.
        short_window (int): Short window for moving average calculation.
        long_window (int): Long window for moving average calculation.

    Methods:
        fetch_historical_data(symbol): Fetches historical data for a given symbol.
        calculate_indicators(df): Calculates necessary indicators for the strategy.
        generate_signals(df): Generates buy/sell signals based on the strategy.
        execute_trades(df, symbol): Executes trades based on generated signals.
        run_strategy(): Runs the momentum strategy.
    """

    def __init__(self, api_client, symbols: List[str], short_window: int = 40, long_window: int = 100):
        self.api_client = api_client
        self.symbols = symbols
        self.short_window = short_window
        self.long_window = long_window
        self.logger = logging.getLogger(__name__)

    def fetch_historical_data(self, symbol: str, interval: str = '1h', limit: int = 1000) -> pd.DataFrame:
        """
        Fetches historical data for a given symbol.

        Args:
            symbol (str): The trading symbol.
            interval (str): The time interval for the data.
            limit (int): The number of data points to fetch.

        Returns:
            pd.DataFrame: Historical data.
        """
        data = self.api_client.get_historical_data(symbol, interval=interval, limit=limit)
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df

    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates necessary indicators for the strategy.

        Args:
            df (pd.DataFrame): Historical data.

        Returns:
            pd.DataFrame: Data with calculated indicators.
        """
        df['short_mavg'] = df['close'].rolling(window=self.short_window, min_periods=1).mean()
        df['long_mavg'] = df['close'].rolling(window=self.long_window, min_periods=1).mean()
        return df

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generates buy/sell signals based on the strategy.

        Args:
            df (pd.DataFrame): Data with calculated indicators.

        Returns:
            pd.DataFrame: Data with generated signals.
        """
        df['signal'] = 0
        df['signal'][self.short_window:] = np.where(df['short_mavg'][self.short_window:] > df['long_mavg'][self.short_window:], 1, 0)
        df['positions'] = df['signal'].diff()
        return df

    def execute_trades(self, df: pd.DataFrame, symbol: str) -> None:
        """
        Executes trades based on generated signals.

        Args:
            df (pd.DataFrame): Data with generated signals.
            symbol (str): The trading symbol.
        """
        for index, row in df.iterrows():
            if row['positions'] == 1:
                self.api_client.buy(symbol, 1)
                self.logger.info(f"Executed BUY for {symbol} at {row['close']}")
            elif row['positions'] == -1:
                self.api_client.sell(symbol, 1)
                self.logger.info(f"Executed SELL for {symbol} at {row['close']}")

    def run_strategy(self) -> None:
        """
        Runs the momentum strategy.
        """
        for symbol in self.symbols:
            df = self.fetch_historical_data(symbol)
            df = self.calculate_indicators(df)
            df = self.generate_signals(df)
            self.execute_trades(df, symbol)
