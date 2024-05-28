import unittest
from bot import BreadBot
from config.settings import INFURA_URL, WALLETS, EXCHANGES, API_BASE_URL, API_KEY
from util.market_analysis import MarketAnalysisTools
from util.risk_management import EnhancedRiskManagement
from util.exchange_api import ExchangeAPI

class TestBreadBot(unittest.TestCase):
    def setUp(self):
        self.breadbot = BreadBot(
            INFURA_URL,
            WALLETS,
            EXCHANGES,
            MarketAnalysisTools(),
            EnhancedRiskManagement(0.2, 0.1, 100000),
            ExchangeAPI(API_BASE_URL, API_KEY)
        )

    def test_should_buy(self):
        # Example test case for should_buy method
        result = self.breadbot.should_buy("BTC/USD", 45000)
        self.assertIsInstance(result, bool)

    def test_should_sell(self):
        # Example test case for should_sell method
        result = self.breadbot.should_sell("BTC/USD", 45000)
        self.assertIsInstance(result, bool)

if __name__ == '__main__':
    unittest.main()
