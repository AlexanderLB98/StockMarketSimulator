# from broker import Broker
# from strategy import Strategy
# from share import Share

class Portfolio():
    def __init__(self, capital: float = 1000):
        # super().__init__(strategy, capital)
        self.shares = []
        self.options = 0
        self.capital_inicial = capital
        self.capital = capital  
        
    def reset(self):
        self.capital = self.capital_inicial
        self.shares = []
        self.options = 0
        
        
    def update_capital(self, reward):
        self.capital += reward
        
    def buy_share(self, market):
        # self.shares += 1
        self.capital -= market.current_price
        
        share = {
            "ID": "_".join([market.name, market.date]),
            "share_name": market.name,
            "buy_price": market.current_price,
            "buy_date": market.date
        }
        
        self.shares.append(share)
        

        
    def sell_available(self, market):
        """_summary_
            Este metodo comprobará si hay alguna acción 
            para vender con profit.
            Para ello, recorrerá todas las acciones 
            (posteriormente será un doble bucle, uno de 
            compañías, y otro de todas las acciones por compaía)
            Comparará los precios de compra con el actual, y 
            validará si son aptos para la venta.
            
            Tengo que decidir si esto devuelve la que se vende
            por más valor, o devolverlas todas. El primer caso
            es mucho más facil, pero no se qué implicaciones
            puede tener a futuro.
        """
        
        max_profit = float("-inf")
        for i, share in enumerate(self.shares):
            buy_price = share.get("buy_price")
            profit = market.current_price - buy_price
            if profit > max_profit:
                max_profit = profit
                max_profit_index = i
            # if buy_price < current_price:
            #     print(f'Se puede vender la acción {share["name"]} '
            #             f'comprada el día {share["buy_date"]} '
            #             f'por {share["buy_value"]}')
        return max_profit, max_profit_index
                
        
        
    def sell_share(self, market):
        max_profit, max_profit_index = self.sell_available(market)
        
        # Solo venderá si el profit es mayor que X
        if max_profit > 50:
            self.shares.pop(max_profit_index)
            self.capital += max_profit
            return True
            
        #self.shares -= 1
        #self.capital += market.current_price
        return False

    def add_option(self):
        pass
    
    def remove_option(self):
        pass        