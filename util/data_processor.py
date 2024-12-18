"""
Data Processor

This module provides a class for processing and analyzing data fetched from various sources.

To-Do:
- Implement additional data processing methods as needed.
- Add unit tests for each data processing method.
"""

from datetime import datetime
from typing import List, Union
import logging

logging.basicConfig(level=logging.INFO)

class DataProcessor:
    """
    A class for processing and analyzing data fetched from various sources.

    Attributes:
        None
    """

    @staticmethod
    def calculate_average(data: List[float]) -> Union[float, None]:
        """
        Calculates the average of a list of numeric data.

        Args:
            data (List[float]): List of numeric data.

        Returns:
            float or None: Average of the data if successful, None otherwise.
        """
        try:
            if not data:
                logging.error("Error calculating average: Data is empty.")
                return None
            return sum(data) / len(data)
        except Exception as e:
            logging.error(f"Error calculating average: {e}")
            return None

    @staticmethod
    def format_date(timestamp: int) -> Union[str, None]:
        """
        Formats a timestamp into a human-readable date string.

        Args:
            timestamp (int): Unix timestamp.

        Returns:
            str or None: Formatted date string if successful, None otherwise.
        """
        try:
            if not timestamp:
                logging.error("Error formatting date: Timestamp is empty.")
                return None
            return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            logging.error(f"Error formatting date: {e}")
            return None

    @staticmethod
    def remove_outliers(data: List[float], threshold: int = 3) -> Union[List[float], None]:
        """
        Removes outliers from a list of numeric data.

        Args:
            data (List[float]): List of numeric data.
            threshold (int): Number of standard deviations from the mean to consider as an outlier.

        Returns:
            List[float] or None: Data without outliers if successful, None otherwise.
        """
        try:
            if not data:
                logging.error("Error removing outliers: Data is empty.")
                return None
            mean = sum(data) / len(data)
            std_dev = (sum((x - mean) ** 2 for x in data) / len(data)) ** 0.5
            filtered_data = [x for x in data if abs(x - mean) <= threshold * std_dev]
            return filtered_data
        except Exception as e:
            logging.error(f"Error removing outliers: {e}")
            return None
