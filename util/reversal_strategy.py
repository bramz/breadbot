import pandas as pd
from typing import List
import logging

logging.basicConfig(level=logging.INFO)

class ReversalStrategyUtility:
    """
    Implements a reversal indicator strategy for trading cryptocurrencies.

    Attributes:
        api_client (APIClient): Client for interacting with exchange APIs.
        symbols (List[str]): List of symbols to trade.
        cci_length (int): Length for CCI calculation.
        rsi_length (int): Length for RSI calculation.
        rsi_overbought (int): RSI overbought level.
        rsi_oversold (int): RSI oversold level.

    Methods:
        fetch_historical_data(symbol): Fetches historical data for a given symbol.
        calculate_indicators(df): Calculates necessary indicators for the strategy.
        generate_signals(df): Generates buy/sell signals based on the strategy.
        execute_trades(df, symbol): Executes trades based on generated signals.
        run_strategy(): Runs the reversal indicator strategy.
    """

    def __init__(self, api_client, symbols: List[str], cci_length: int = 14, rsi_length: int = 14,
                 rsi_overbought: int = 70, rsi_oversold: int = 30):
        self.api_client = api_client
        self.symbols = symbols
        self.cci_length = cci_length
        self.rsi_length = rsi_length
        self.rsi_overbought = rsi_overbought
        self.rsi_oversold = rsi_oversold
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
        df['cci'] = ((df['close'] - df['close'].rolling(window=self.cci_length).mean()) / 
                     (0.015 * df['close'].rolling(window=self.cci_length).std()))
        df['rsi'] = self.calculate_rsi(df['close'])
        return df

    def calculate_rsi(self, prices: pd.Series) -> pd.Series:
        """
        Calculates the Relative Strength Index (RSI).

        Args:
            prices (pd.Series): Series of prices.

        Returns:
            pd.Series: RSI values.
        """
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_length).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_length).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generates buy/sell signals based on the strategy.

        Args:
            df (pd.DataFrame): Data with calculated indicators.

        Returns:
            pd.DataFrame: Data with generated signals.
        """
        df['signal'] = 0
        df['signal'] = df.apply(self.check_conditions, axis=1)
        return df

    def check_conditions(self, row):
        """
        Check the conditions for generating buy/sell signals.

        Args:
            row (pd.Series): Row of data.

        Returns:
            int: Signal (1 for buy, -1 for sell, 0 for hold).
        """
        if row['cci'] > 100 and row['rsi'] > self.rsi_overbought:
            return -1
        elif row['cci'] < -100 and row['rsi'] < self.rsi_oversold:
            return 1
        return 0

    def execute_trades(self, df: pd.DataFrame, symbol: str) -> None:
        """
        Executes trades based on generated signals.

        Args:
            df (pd.DataFrame): Data with generated signals.
            symbol (str): The trading symbol.
        """
        for index, row in df.iterrows():
            if row['signal'] == 1:
                self.api_client.buy(symbol, 1)
                self.logger.info(f"Executed BUY for {symbol} at {row['close']}")
            elif row['signal'] == -1:
                self.api_client.sell(symbol, 1)
                self.logger.info(f"Executed SELL for {symbol} at {row['close']}")

    def run_strategy(self) -> None:
        """
        Runs the reversal indicator strategy.
        """
        for symbol in self.symbols:
            df = self.fetch_historical_data(symbol)
            df = self.calculate_indicators(df)
            df = self.generate_signals(df)
            self.execute_trades(df, symbol)
