"""
Market Analysis Tools

This module provides tools for market analysis, including sentiment analysis, trend analysis, and technical indicators.
"""

import numpy as np
from util.risk_management import MovingAverage

class SentimentAnalysis:
    """
    Provides methods for sentiment analysis based on news data.
    """
    @staticmethod
    def analyze_news_sentiment(news_data):
        """
        Analyzes sentiment scores from news data.

        Args:
            news_data (list of dict): List of news articles with sentiment scores.

        Returns:
            float: Average sentiment score.
        """
        sentiment_scores = [article["sentiment"] for article in news_data]
        average_sentiment = sum(sentiment_scores) / len(sentiment_scores)
        return average_sentiment

    @staticmethod
    def calculate_market_sentiment_index(sentiment_scores):
        """
        Calculates market sentiment index from sentiment scores.

        Args:
            sentiment_scores (list of float): List of sentiment scores.

        Returns:
            float: Market sentiment index.
        """
        return sum(sentiment_scores) / len(sentiment_scores)

class TrendingStrategy:
    """
    Implements trend analysis strategies using moving averages.
    """
    def __init__(self, moving_average_period):
        self.moving_average_period = moving_average_period

    def is_above_moving_average(self, current_price, moving_average_data):
        """
        Checks if the current price is above the moving average.

        Args:
            current_price (float): Current price.
            moving_average_data (list of float): Moving average data.

        Returns:
            bool: True if above the moving average, False otherwise.
        """
        moving_avg = MovingAverage.calculate_simple_moving_average(moving_average_data, self.moving_average_period)
        return current_price > moving_avg

    def is_below_moving_average(self, current_price, moving_average_data):
        """
        Checks if the current price is below the moving average.

        Args:
            current_price (float): Current price.
            moving_average_data (list of float): Moving average data.

        Returns:
            bool: True if below the moving average, False otherwise.
        """
        moving_avg = MovingAverage.calculate_simple_moving_average(moving_average_data, self.moving_average_period)
        return current_price < moving_avg


class MarketAnalysisTools:
    """
    Provides various tools for market analysis.
    """
    @staticmethod
    def calculate_macd(prices, short_window=12, long_window=26, signal_window=9):
        """
        Calculates the Moving Average Convergence Divergence (MACD).

        Args:
            prices (list of float): List of historical prices.
            short_window (int): Short-term moving average window size.
            long_window (int): Long-term moving average window size.
            signal_window (int): Signal line window size.

        Returns:
            tuple: MACD line and signal line.
        """
        ema_short = MovingAverage.calculate_moving_average(prices, short_window)
        ema_long = MovingAverage.calculate_moving_average(prices, long_window)
        macd_line = ema_short - ema_long
        signal_line = MovingAverage.calculate_moving_average(macd_line, signal_window)
        return macd_line, signal_line

    @staticmethod
    def calculate_ema(prices, window_size):
        """
        Calculates the Exponential Moving Average (EMA).

        Args:
            prices (list of float): List of historical prices.
            window_size (int): EMA window size.

        Returns:
            list of float: EMA values.
        """
        return MovingAverage.calculate_moving_average(prices, window_size)

    @staticmethod
    def calculate_atr(prices, window_size=14):
        """
        Calculates the Average True Range (ATR).

        Args:
            prices (list of float): List of historical prices.
            window_size (int): ATR window size.

        Returns:
            float: ATR value.
        """
        if len(prices) <= window_size:
            return 0  # Default ATR
        true_range = [max(prices[i + 1], prices[i]) - min(prices[i + 1], prices[i]) for i in range(len(prices) - 1)]
        atr = sum(true_range[-window_size:]) / window_size
        return atr

    @staticmethod
    def calculate_bollinger_bands(prices, window_size=20, num_std_dev=2):
        """
        Calculates Bollinger Bands.

        Args:
            prices (list of float): List of historical prices.
            window_size (int): Window size for calculating the moving average.
            num_std_dev (int): Number of standard deviations for the bands.

        Returns:
            tuple: Upper band and lower band.
        """
        if len(prices) < window_size:
            return 0, 0  # Default values for bands
        sma = MovingAverage.calculate_moving_average(prices, window_size)
        std_dev = np.std(prices[-window_size:])
        upper_band = sma + (num_std_dev * std_dev)
        lower_band = sma - (num_std_dev * std_dev)
        return upper_band, lower_band
