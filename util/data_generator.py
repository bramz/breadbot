import random
from typing import List, Dict, Any
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)

class DataGenerator:
    """
    A class for generating historical crypto data for backtesting and analysis.

    Attributes:
        symbols (List[str]): List of symbols to generate data for.
        start_date (datetime): Start date for data generation.
        end_date (datetime): End date for data generation.
    """

    def __init__(self, symbols: List[str], start_date: str, end_date: str):
        """
        Initialize DataGenerator with necessary parameters.

        Parameters:
            symbols (List[str]): List of symbols to generate data for.
            start_date (str): Start date for data generation (YYYY-MM-DD).
            end_date (str): End date for data generation (YYYY-MM-DD).
        """
        try:
            self.symbols = symbols
            self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
            self.end_date = datetime.strptime(end_date, "%Y-%m-%d")
            if self.start_date > self.end_date:
                raise ValueError("Start date must be before end date.")
            logging.info("DataGenerator initialized successfully.")
        except ValueError as e:
            logging.error(f"Error in initializing DataGenerator: {e}")
            raise

    def generate_data(self) -> List[Dict[str, Any]]:
        """
        Generate historical crypto data for backtesting and analysis.

        Returns:
            List[Dict[str, Any]]: List of dictionaries containing historical data points.
        """
        historical_data = []
        current_date = self.start_date
        while current_date <= self.end_date:
            data_point = {"date": current_date.strftime("%Y-%m-%d")}
            for symbol in self.symbols:
                data_point[symbol] = random.uniform(10, 10000)  # Random price for demo purposes
            historical_data.append(data_point)
            current_date += timedelta(days=1)
        logging.info("Data generation completed successfully.")
        return historical_data
