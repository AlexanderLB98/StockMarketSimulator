"""_summary_
        Class to render everything
"""

from src.Market import Market
from src.Broker import Broker

class Render:
    def __init__(self,
                 market: Market,
                 broker: Broker
                 ):
        
        self.market = market
        self.broker = broker
        
        
    def render(self, action):
        
        self.market.render(action = action)
        self.broker.render()
        
    
    