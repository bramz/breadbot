import statistics
import numpy as np

class StopLoss:
    def __init__(self, threshold):
        self.threshold = threshold

    def check_stop_loss(self, current_price, entry_price):
        return current_price <= entry_price * (1 - self.threshold)

class TrailingStop:
    def __init__(self, trail_percent):
        self.trail_percent = trail_percent
        self.highest_price = float("-inf")

    def update_trailing_stop(self, current_price):
        self.highest_price = max(self.highest_price, current_price)
        return self.highest_price * (1 - self.trail_percent)

class PositionSizing:
    def __init__(self, risk_per_trade, max_drawdown):
        self.risk_per_trade = risk_per_trade
        self.max_drawdown = max_drawdown

    def calculate_trade_size(self, account_balance, stop_loss_price):
        risk_amount = account_balance * self.risk_per_trade
        trade_size = risk_amount / (account_balance - stop_loss_price)
        return min(trade_size, account_balance * self.max_drawdown)

class TrendAnalysis:
    @staticmethod
    def is_above_moving_average(current_price, avg_price):
        return current_price > avg_price

class VolatilityAnalysis:
    @staticmethod
    def is_above_standard_deviation(current_price, avg_price, price_std_dev, deviation_factor=1.5):
        return current_price > avg_price + (deviation_factor * price_std_dev)

class RSIAnalysis:
    @staticmethod
    def is_oversold(prices, threshold=30):
        rsi = RSIAnalysis.calculate_rsi(prices)
        return rsi < threshold

    @staticmethod
    def calculate_rsi(prices):
        if len(prices) < 2:
            return 0

        gains = [prices[i + 1] - prices[i] for i in range(len(prices) - 1) if prices[i + 1] > prices[i]]
        losses = [-1 * (prices[i + 1] - prices[i]) for i in range(len(prices) - 1) if prices[i + 1] < prices[i]]

        avg_gain = sum(gains) / len(gains) if gains else 0
        avg_loss = sum(losses) / len(losses) if losses else 0

        if avg_loss == 0:
            return 100

        relative_strength = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + relative_strength))

        return rsi

class ResistanceAnalysis:
    @staticmethod
    def calculate_resistance_level(prices):
        return max(prices)

class SentimentAnalysis:
    @staticmethod
    def is_positive_sentiment():
        return True

class VolumeAnalysis:
    @staticmethod
    def is_volume_increasing():
        return True

class MovingAverage:
    @staticmethod
    def calculate_moving_average(prices, window_size):
        if len(prices) < window_size:
            return 0
        return sum(prices[-window_size:]) / window_size
    
class Diversification:
    @staticmethod
    def is_diversified(portfolio):
        return len(set(portfolio)) > 1  # Check if the portfolio contains more than one unique asset


class CorrelationAnalysis:
    @staticmethod
    def calculate_correlation(asset1_prices, asset2_prices):
        correlation = statistics.corrcoef(asset1_prices, asset2_prices)[0, 1]  # Calculate the correlation coefficient between asset price movements
        return correlation


class MarketSentimentAnalysis:
    @staticmethod
    def analyze_market_sentiment(news_data):
        # Placeholder sentiment analysis logic
        sentiment_score = sum(article["sentiment"] for article in news_data) / len(news_data)
        return sentiment_score


class LiquidityAnalysis:
    @staticmethod
    def assess_market_liquidity(volume_data):
        average_volume = sum(volume_data) / len(volume_data)
        if average_volume > 100000:  # Example threshold for liquidity
            is_liquid = True
        else:
            is_liquid = False
        return is_liquid


class EventRiskManagement:
    @staticmethod
    def manage_event_risk(event_data):
        risk_level = event_data["impact"]  # Example: Event impact level from event data
        return risk_level


class DynamicPositionSizing:
    @staticmethod
    def adjust_position_size(account_balance, volatility, market_conditions):
        if market_conditions["volatility"] > 0.1:  # Example threshold for high volatility
            position_size = account_balance * 0.05  # Allocate 5% of account balance for trading in high volatility
        else:
            position_size = account_balance * 0.1  # Allocate 10% of account balance for trading in normal volatility
        return position_size


class HedgingStrategies:
    @staticmethod
    def implement_hedging(portfolio, market_conditions):
        if market_conditions["sentiment_score"] < 0.5:  # Example threshold for negative sentiment
            hedged_portfolio = [asset + "_hedged" for asset in portfolio]  # Placeholder: Apply hedging to each asset
        else:
            hedged_portfolio = portfolio  # No hedging applied
        return hedged_portfolio
    
class TechnicalIndicators:
    def calculate_bollinger_bands(prices, window_size=20, num_std_dev=2):
        if len(prices) < window_size:
            return 0, 0  # Default values for bands
        sma = MovingAverage.calculate_moving_average(prices, window_size)
        std_dev = np.std(prices[-window_size:])
        upper_band = sma + (num_std_dev * std_dev)
        lower_band = sma - (num_std_dev * std_dev)
        return upper_band, lower_band