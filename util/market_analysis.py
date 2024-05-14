# market_analysis.py

import numpy as np
from util.risk_management import MovingAverage

class SentimentAnalysis:
    @staticmethod
    def analyze_news_sentiment(news_data):
        sentiment_scores = [article["sentiment"] for article in news_data]
        average_sentiment = sum(sentiment_scores) / len(sentiment_scores)
        return average_sentiment

    @staticmethod
    def calculate_market_sentiment_index(sentiment_scores):
        return sum(sentiment_scores) / len(sentiment_scores)

class TrendingStrategy:
    def __init__(self, moving_average_period):
        self.moving_average_period = moving_average_period

    def is_above_moving_average(self, current_price, moving_average_data):
        moving_avg = MovingAverage.calculate_simple_moving_average(moving_average_data, self.moving_average_period)
        return current_price > moving_avg

    def is_below_moving_average(self, current_price, moving_average_data):
        moving_avg = MovingAverage.calculate_simple_moving_average(moving_average_data, self.moving_average_period)
        return current_price < moving_avg


class MarketAnalysisTools:
    @staticmethod
    def calculate_macd(prices, short_window=12, long_window=26, signal_window=9):
        ema_short = MovingAverage.calculate_moving_average(prices, short_window)
        ema_long = MovingAverage.calculate_moving_average(prices, long_window)
        macd_line = ema_short - ema_long
        signal_line = MovingAverage.calculate_moving_average(macd_line, signal_window)
        return macd_line, signal_line

    @staticmethod
    def calculate_ema(prices, window_size):
        return MovingAverage.calculate_moving_average(prices, window_size)

    @staticmethod
    def calculate_atr(prices, window_size=14):
        if len(prices) <= window_size:
            return 0  # Default ATR
        true_range = [max(prices[i + 1], prices[i]) - min(prices[i + 1], prices[i]) for i in range(len(prices) - 1)]
        atr = sum(true_range[-window_size:]) / window_size
        return atr

    @staticmethod
    def calculate_bollinger_bands(prices, window_size=20, num_std_dev=2):
        if len(prices) < window_size:
            return 0, 0  # Default values for bands
        sma = MovingAverage.calculate_moving_average(prices, window_size)
        std_dev = np.std(prices[-window_size:])
        upper_band = sma + (num_std_dev * std_dev)
        lower_band = sma - (num_std_dev * std_dev)
        return upper_band, lower_band