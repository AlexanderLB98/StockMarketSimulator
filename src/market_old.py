import matplotlib.pyplot as plt

from src.portfolio import Portfolio
from dataAdquisition.dataAdquisition import DataAdquisition

class Market():
    
    # Define los colores y las acciones como variables de clase
    COLORS = {0: 'k',  # Negro para HOLD
              1: 'g',  # Verde para BUY
              2: 'r'}  # Rojo para SELL

    ACTIONS = {0: 'HOLD',
               1: 'BUY',
               2: 'SELL'}
    
    
    def __init__(self, dataAdquisition: DataAdquisition = DataAdquisition("offline"), portfolio: Portfolio = None) :
        self.dataAdquisition = dataAdquisition
        self.companies = []
        self.timestep = 0
        self.plot_created = False
        self.portfolio = portfolio
        self.name = "AEX"
        
        
    def _initialize_variables(self):
        obs = []
        self.timestep = 0
        self.plot_created = False
        self.done = False
        self._initialize_fig()
        return obs
        
    def reset(self):
        obs = self._initialize_variables()
        self.dataAdquisition.reset()
        print("Reseting...")
        return obs, False
    
    def step(self, action):
        # next_obs = []
        
        next_obs, done = self.dataAdquisition.step()
        #reward = {}
        total_reward = 0
        self.dataAdquisition.step()
        
        # Obtener el precio actual del activo
        self.current_price = self.dataAdquisition.get_current_data()["Close"]
        reward = 0
        
        # Calcular la recompensa
        if action == 1:  # BUY
            if self.portfolio.capital >= self.current_price:
                self.portfolio.buy_share(self)
                # self.portfolio.capital -= current_price
                reward = -self.current_price
            else:
                print("No tienes peras para comprar la accion parguela.\n")
                print(f"Te faltan {self.current_price - self.portfolio.capital: .2f} euros pa comprarla")
                print("Pasando a Hold")
                action = 0
                reward = 0
        elif action == 2:  # SELL
            if self.portfolio.shares > 0:
            # self.portfolio.capital += self.current_price
                self.portfolio.sell_share(self)
                reward = self.current_price
            else:
                print(f"No puedes vender por que no tienes acciones de la empresa {self.name}")
                print("Se pasa a Hold")
                action = 0
                reward = 0
        #else:  # HOLD
            
        
        
        self.timestep += 1
        if self.timestep > 100:
            done = True
        return next_obs, total_reward, reward, done
    
            
    def _initialize_fig(self):
        # Si el gráfico no ha sido creado todavía, crearlo y mostrar el primer punto
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(211)
        self.ax.set_title("Estado actual del mercado")
        self.ax.set_xlabel("Paso")
        self.ax.set_ylabel("Precio")
        self.ax.grid()
        self.plot_created = True
            

    def render(self, action):
        current_data = self.dataAdquisition.get_current_data()["Close"]
        # print("Rendering..." + str(self.timestep) + " and data: " + str(current_data))
        if current_data is not None:
            if not self.plot_created:
                self.plot_created = True
            
            # Obtén el color y la acción correspondiente
            color = self.COLORS[action]
            action_label = self.ACTIONS[action]
            
            # Si el gráfico ya fue creado, simplemente añadir un punto al gráfico existente
            self.ax.plot(self.timestep, current_data, color + 'o', label=action_label)
            plt.pause(0.01)  # Pausa para actualizar el gráfico
        else:
            print("No hay datos disponibles para renderizar en el mercado.")
