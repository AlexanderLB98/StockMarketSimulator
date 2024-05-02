


from src.broker import Broker
from src.company import Company
from src.dataAdquisition.dataAdquisition import DataAdquisition
#from src.dataAdquisition.dataAdquisition import DataAdquisition
from src.market_old import Market
#from src.market import Market
from src.portfolio import Portfolio
from src.strategy import Strategy


# Define el diccionario de acciones globalmente
actions = {0: 'HOLD',
           1: 'BUY',
           2: 'SELL'}


def sim():
    # Configuración inicial. Esto en un futuro saldrá de un json
    initial_capital = 1000 # En euros
    num_episodes = 1 # numero de episodios, ya sean dias, semanas, o lo que sea el dt que represente el método step de la clase market
    
    
    # Se instancia la estrategia
    strategy = Strategy()
    
    # Se instancia el portfolio
    portfolio = Portfolio(strategy = strategy, capital = initial_capital)
    
    # Se instancia el broker
    broker = Broker(strategy = strategy, capital = initial_capital, portfolio = portfolio)
    
    # Definimos el mercado
    market = Market(portfolio = portfolio)
    
    visited = []
    
    rendimientos = {}
    for episode in range(num_episodes):
        obs, done = market.reset()
        portfolio.reset()
        print("Comenzando simulación...")
        while not done:
            action = broker.predict(obs)
            next_obs, total_reward, reward, done = market.step(action)
            obs = next_obs
            visited.append(obs)
            market.render(action=action)
            #print(f"Reward: {reward}")
        print("Simulación terminada con éxito")
        print(f"Capital final de {portfolio.capital: .2f} euros\n")
        rendimiento = portfolio.capital/portfolio.capital_inicial
        print(f"Rendimiento: {rendimiento: .2f}")
        rendimientos[f"Sim_{episode}"] = rendimiento
        
    print(rendimientos)
    max_key = max(rendimientos, key=rendimientos.get)
    max_reward = rendimientos[max_key]
    print(f"Mejor episodio: {max_key} con recompensa: {max_reward}")
    
    return visited
        
if __name__ == "__main__":
    obs = sim()
    print(obs)