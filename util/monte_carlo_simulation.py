# util/monte_carlo_simulation.py

import numpy as np
from typing import List

class MonteCarloSimulation:
    def __init__(self, initial_balance: float, num_simulations: int, num_days: int):
        """
        Initialize MonteCarloSimulation with necessary parameters.

        Parameters:
        - initial_balance (float): Initial account balance.
        - num_simulations (int): Number of simulations to run.
        - num_days (int): Number of days to simulate.
        """
        self.initial_balance = initial_balance
        self.num_simulations = num_simulations
        self.num_days = num_days

    def simulate(self, mean_return: float, std_dev: float) -> List[float]:
        """
        Run Monte Carlo simulations to project future account balances.

        Parameters:
        - mean_return (float): Mean daily return.
        - std_dev (float): Standard deviation of daily returns.

        Returns:
        - List[float]: Simulated account balances at the end of the simulation period.
        """
        simulations = []
        for _ in range(self.num_simulations):
            daily_returns = np.random.normal(mean_return, std_dev, self.num_days)
            balance = self.initial_balance
            for daily_return in daily_returns:
                balance *= (1 + daily_return)
            simulations.append(balance)
        return simulations
