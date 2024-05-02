import gymnasium as gym
from src.render.Render import Render
from src.render.render_figures import RenderFigures

class Market(gym.Env):
    
    def __init__(self, brokers: list, render: Render):
        # brokers = [broker1, broker2, broker3]  
        self.brokers = brokers
        self.render_class = render