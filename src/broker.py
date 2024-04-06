import numpy as np

from src.strategy import Strategy

class Broker():
    def __init__(self, strategy: Strategy, capital: float = 1000, portfolio= None):
        self.strategy = strategy
        self.capital = capital # Por defecto 1000 euros
        
    def predict(self, obs):
        """_summary_
            Predicts the next action:
                - 0: hold
                - 1: buy
                - 2: sell
        Returns:
            int: Hold, buy or sell action
        """
        action = np.random.randint(3)
        
        
        return action
        
    def buy_share(self, option):
        pass
    
    def sell_share(self, option):
        pass
    
    def buy_option(self, option):
        pass
    
    def sell_option(self, option):
        pass