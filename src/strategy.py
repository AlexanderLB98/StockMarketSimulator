from statistics import mean
# from market import Market
# from portfolio import Portfolio

class Strategy():
    def __init__(self, portfolio = None):
        self.portfolio = portfolio
        self.buffer = []
        # self.market = market
                
    def decide_action(self, market):
        
        current_price = market.current_price
        last_price = market.last_price
        
        cost = self.calculate_cost_per(current_price, self.portfolio.capital)
        
        if len(self.buffer) < 1:
            diff = current_price - last_price # Positivo es que sube el valor
        else:
            diff = mean(self.buffer)
        
        if (diff > 0) & (cost < 0.1): # el precio sube, comprar
            optim_action = 1 # Buy
            print("La accion óptima sería comprar")
        else: 
            """
            Lo siguiente sería implementar en la estrategia 
            un calculo del profit al vender la accion, para 
            que no venda siemrpe. Para ello, habrá que añadir 
            una mecanica que a la hora de comprar una accion, 
            en ungar de share+1, añadir un diccionario, con la 
            accion, alomejor informacion de la fecha de ocmpra, 
            y e lvalor de la compra, y con ese precio calcular 
            el profi, y solo vender si profit > 20% por ejemplo 
            (ajustar para ser mas o menos consrvador)
            """
            optim_action = 2 # Sell
            print("La accion óptima sería vender")
        
        self.buffer.append(current_price)
        
        return optim_action
    
    def calculate_cost_per(self, stock_price, capital):
        return stock_price / capital

    
        