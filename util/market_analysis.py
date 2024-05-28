"""
Market Analysis Tools

This module provides tools for market analysis, including sentiment analysis, trend analysis, and technical indicators.
"""

import numpy as np
from util.risk_management import MovingAverage
import logging
from typing import List, Dict, Tuple

logging.basicConfig(level=logging.INFO)  # Configure logging

class SentimentAnalysis:
    """
    Provides methods for sentiment analysis based on news data.
    """
    @staticmethod
    def analyze_news_sentiment(news_data: List[Dict[str, float]]) -> float:
        """
        Analyzes sentiment scores from news data.

        Args:
            news_data (list of dict): List of news articles with sentiment scores.

        Returns:
            float: Average sentiment score.
        """
        try:
            sentiment_scores = [article["sentiment"] for article in news_data]
            average_sentiment = sum(sentiment_scores) / len(sentiment_scores)
            return average_sentiment
        except (KeyError, TypeError) as e:
            logging.error(f"Error in analyzing news sentiment: {str(e)}")
            return 0.0

    @staticmethod
    def calculate_market_sentiment_index(sentiment_scores: List[float]) -> float:
        """
        Calculates market sentiment index from sentiment scores.

        Args:
            sentiment_scores (list of float): List of sentiment scores.

        Returns:
            float: Market sentiment index.
        """
        try:
            return sum(sentiment_scores) / len(sentiment_scores)
        except ZeroDivisionError:
            logging.warning("Empty sentiment scores list.")
            return 0.0

class TrendingStrategy:
    """
    Implements trend analysis strategies using moving averages.
    """
    def __init__(self, moving_average_period: int):
        self.moving_average_period = moving_average_period

    def is_above_moving_average(self, current_price: float, moving_average_data: List[float]) -> bool:
        """
        Checks if the current price is above the moving average.

        Args:
            current_price (float): Current price.
            moving_average_data (list of float): Moving average data.

        Returns:
            bool: True if above the moving average, False otherwise.
        """
        try:
            moving_avg = MovingAverage.calculate_moving_average(moving_average_data, self.moving_average_period)
            return current_price > moving_avg
        except ZeroDivisionError:
            logging.error("Error in calculating moving average: Zero division error.")
            return False

    def is_below_moving_average(self, current_price: float, moving_average_data: List[float]) -> bool:
        """
        Checks if the current price is below the moving average.

        Args:
            current_price (float): Current price.
            moving_average_data (list of float): Moving average data.

        Returns:
            bool: True if below the moving average, False otherwise.
        """
        try:
            moving_avg = MovingAverage.calculate_moving_average(moving_average_data, self.moving_average_period)
            return current_price < moving_avg
        except ZeroDivisionError:
            logging.error("Error in calculating moving average: Zero division error.")
            return False

class MarketAnalysisTools:
    """
    Provides various tools for market analysis.
    """
    @staticmethod
    def calculate_macd(prices: List[float], short_window: int = 12, long_window: int = 26, signal_window: int = 9) -> Tuple[float, float]:
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
        try:
            ema_short = MovingAverage.calculate_moving_average(prices, short_window)
            ema_long = MovingAverage.calculate_moving_average(prices, long_window)
            macd_line = ema_short - ema_long
            signal_line = MovingAverage.calculate_moving_average(macd_line, signal_window)
            return macd_line, signal_line
        except Exception as e:
            logging.error(f"Error in calculating MACD: {str(e)}")
            return 0.0, 0.0

    @staticmethod
    def calculate_ema(prices: List[float], window_size: int) -> List[float]:
        """
        Calculates the Exponential Moving Average (EMA).

        Args:
            prices (list of float): List of historical prices.
            window_size (int): EMA window size.

        Returns:
            list of float: EMA values.
        """
        try:
            return MovingAverage.calculate_moving_average(prices, window_size)
        except Exception as e:
            logging.error(f"Error in calculating EMA: {str(e)}")
            return []

    @staticmethod
    def calculate_atr(prices: List[float], window_size: int = 14) -> float:
        """
        Calculates the Average True Range (ATR).

        Args:
            prices (list of float): List of historical prices.
            window_size (int): ATR window size.

        Returns:
            float: ATR value.
        """
        try:
            if len(prices) <= window_size:
                return 0.0  # Default ATR
            true_range = [max(prices[i + 1], prices[i]) - min(prices[i + 1], prices[i]) for i in range(len(prices) - 1)]
            atr = sum(true_range[-window_size:]) / window_size
            return atr
        except Exception as e:
            logging.error(f"Error in calculating ATR: {str(e)}")
            return 0.0

    @staticmethod
    def calculate_bollinger_bands(prices: List[float], window_size: int = 20, num_std_dev: int = 2) -> Tuple[float, float]:
        """
        Calculates Bollinger Bands.

        Args:
            prices (list of float): List of historical prices.
            window_size (int): Window size for calculating the moving average.
            num_std_dev (int): Number of standard deviations for the bands.

        Returns:
            tuple: Upper band and lower band.
        """
        try:
            if len(prices) < window_size:
                return 0.0, 0.0  # Default values for bands
            sma = MovingAverage.calculate_moving_average(prices, window_size)
            std_dev = np.std(prices[-window_size:])
            upper_band = sma + (num_std_dev * std_dev)
            lower_band = sma - (num_std_dev * std_dev)
            return upper_band, lower_band
        except Exception as e:
            logging.error(f"Error in calculating Bollinger Bands: {str(e)}")
            return 0.0, 0.0
