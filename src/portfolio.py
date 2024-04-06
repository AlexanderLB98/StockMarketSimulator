from src.broker import Broker
from src.strategy import Strategy



class Portfolio(Broker):
    def __init__(self, strategy: Strategy, capital: float = 1000):
        super().__init__(strategy, capital)
        self.shares = 0
        self.options = 0
        self.capital_inicial = capital
        self.capital = capital  
        
    def reset(self):
        self.capital = self.capital_inicial
        self.shares = 0
        self.options = 0
        
        
    def update_capital(self, reward):
        self.capital += reward
        
    def buy_share(self, market):
        self.shares += 1
        self.capital -= market.current_price
        
    def sell_share(self, market):
        self.shares -= 1
        self.capital -= market.current_price
        

    def add_option(self):
        pass
    
    def remove_option(self):
        pass        