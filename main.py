import tkinter as tk

from src.Company import Company
from src.DataAdquisition import DataAdquisition
from src.Market import Market

from src.Strategy import Strategy
from src.Portfolio import Portfolio
from src.Broker import Broker

from src.Render import Render
from src.GUI import StockSimulatorGUI


# Define el diccionario de acciones globalmente
actions = {0: 'HOLD',
           1: 'BUY',
           2: 'SELL'}


def main():
    # Configuración inicial. Esto en un futuro saldrá de un json
    initial_capital = 10000 # En euros
    num_episodes = 1 # numero de episodios, ya sean dias, semanas, o lo que sea el dt que represente el método step de la clase market
    
    
    
    
    # Se instancia el portfolio
    portfolio = Portfolio(capital = initial_capital)
    
    
    # Se instancia la estrategia
    strategy = Strategy(portfolio = portfolio)
    
    # Se instancia el broker
    broker = Broker(strategy = strategy, capital = initial_capital, portfolio = portfolio)
    
    # Definimos el mercado
    market = Market(portfolio = portfolio, initial_date = "01-01-2016")
    
   
    # Crear la ventana Tkinter
    root = tk.Tk()
    
    # Crear una instancia de la clase GUI y pasarle la ventana, el mercado y el broker
    gui = StockSimulatorGUI(root, market, broker)
    
    # Ejecutar el bucle principal de la aplicación Tkinter
    root.mainloop()

    render = Render(market = market, broker = broker)
    
    
    
    
    
    rendimientos = {}
    for episode in range(num_episodes):
        obs, done = market.reset()
        portfolio.reset()
        print("Comenzando simulación...")
        while not done:
            
            action = broker.predict(obs, market)
            
            market.update_last_price()
            
            next_obs, total_reward, reward, done, fixed_action = market.step(action)
            
            
            
            obs = next_obs
            render.render(action = action)
            # market.render(action=fixed_action)
            print(f"Current capital: {portfolio.capital}")
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
    input("Presiona Enter para terminar...")  # Pausa hasta que el usuario presione Enter
        
if __name__ == "__main__":
    main()