from statistics import mean
# from market import Market
# from portfolio import Portfolio

class Strategy():
    def __init__(self, portfolio = None):
        self.mode = "basic" # "cost": calculates cost respect to total capital
        self.portfolio = portfolio
        self.buffer = [] # Para qué estaba este buffer???? doc
        # self.market = market
                
    def decide_action(self, market):
        
        # current_price = market.current_price #market.current_price es un dict si hay varias compañias
        # last_price = market.last_price
        
        if len(market.companies) == 1:
            # Solo hay una compaía, current price será un valor a convertir en lista
            current_price = [market.current_price]
            last_price = [market.last_price]
        if len(market.companies) > 1:
            current_price = list(market.current_price.values())
            last_price = list(market.last_price.values())

        
        if self.mode == "basic":            
            if len(self.buffer) < 1:
                diff =  [current - last for current, last in zip(current_price, last_price)] # Positivo es que sube el valor
            else:
                """_summary_
                    No se que cojones quería hacer con el buffer, asi que provisionalmente pongo esto
                """
                diff =  [current - last for current, last in zip(current_price, last_price)] # Positivo es que sube el valor
                #diff = mean(self.buffer) # Para qué estaba este buffer???? doc
                
            # diff tendrá que ser una lista de longitud n, siendo n el numro de compañias
            
            # Ahora obtenemos un vector optim_actions de dimensión n(numero compañias), 
            # con la acción óptima para cada compañía
            
            optim_actions = [1 if x > 0 else 2 for x in diff]
            
            self.buffer.append(current_price)
            
            return optim_actions
            """
            if (diff > 0): # el precio sube, comprar
                # optim_action será una lista con las acciones optimas para cada compañía
                
                optim_action = 1 # Buy
                print("La accion óptima sería comprar")
            else: 
                
                Lo siguiente sería implementar en la estrategia 
                un calculo del profit al vender la accion, para 
                que no venda siemrpe. Para ello, habrá que añadir 
                una mecanica que a la hora de comprar una accion, 
                en ungar de share+1, añadir un diccionario, con la 
                accion, alomejor informacion de la fecha de ocmpra, 
                y e lvalor de la compra, y con ese precio calcular 
                el profi, y solo vender si profit > 20% por ejemplo 
                (ajustar para ser mas o menos consrvador)
                
                optim_action = 2 # Sell
                print("La accion óptima sería vender")
            """
            
        elif self.mode == "cost":            
            if len(market.companies) > 1:
                # if there is a list of companies:
                """ 
                    Recorrer todas las compañias, y devolver una lista de costes (o dict)
                """        
            else:
                # If there is only one company:
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
                
                Creo que está implementado, pero en Portfolio. 
                Mover aqui.
                """
                optim_action = 2 # Sell
                print("La accion óptima sería vender")
            
            self.buffer.append(current_price)
            
            return optim_action
        
    def calculate_cost_per(self, stock_price, capital):
        return stock_price / capital

    
        