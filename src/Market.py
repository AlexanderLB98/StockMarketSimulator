import matplotlib.pyplot as plt
import json

# from src.portfolio import Portfolio
from src.DataAdquisition import DataAdquisition# , get_day_yf_data
from src.Utils import DotDict

import yfinance as yf
def get_day_yf_data(company: str = None, date = None):
    # Obtener datos históricos para el índice AEX para la fecha actual
    
    # company = "^AEX"
    # start_date = start_date or getDate("2020-01-10")
    # start_date = start_date or getDate("2021-12-31")
    
    data = yf.download(company, start=date, end=date)

    # Verificar si se obtuvieron datos para el día actual
    if not data.empty:
        # Mostrar los datos más importantes
        first_data = data.iloc[0]
        result = {
            "Compañia": f'AEX --> ({date} ):',
            "Apertura": f': {round(first_data["Open"], 2)}€',
            "Máximo": f': {round(first_data["High"], 2)}€',
            "Mínimo": f': {round(first_data["Low"], 2)}€',
            "Cierre": f': {round(first_data["Close"], 2)}€',
            "Volumen": f': {int(first_data["Volume"])}',
        }
        print(result)
        return data
    else:
        result = 'No hay datos disponibles.'
        assert "No Data from yfinance"
    pass


class Company():
    
    def __init(self, name, initial_price=None):
        self.name = name
        self.initial_price = initial_price
        self.current_price = initial_price
        
    
    

class Market():
    
    # Define los colores y las acciones como variables de clase
    COLORS = {0: 'k',  # Negro para HOLD
              1: 'g',  # Verde para BUY
              2: 'r'}  # Rojo para SELL

    ACTIONS = {0: 'HOLD',
               1: 'BUY',
               2: 'SELL'}
    
    RENDER_MODE = {
        0: 'Individual',
        1: 'MultiCompany'
    }
    
    def __init__(self, 
                 dataAdquisition: DataAdquisition = DataAdquisition("yfinance"), 
                 portfolio = None,
                 initial_date = "01-01-2018") :
        self.dataAdquisition = dataAdquisition
        self.timestep = 0
        self.plot_created = False
        self.portfolio = portfolio
        self.name = "AEX"
        
        self.current_price = {}
        self.last_price = {}
        
        self.initial_date = initial_date
        self.date = self.initial_date
        self.render_mode = 'MultiCompany'
        
    def _load_config(self, config_file):
        with open(config_file) as f:
            self.config = DotDict(json.load(f))
            print(self.config)
        
    def _initialize_companies(self):
        self.companies = self.config.companies
        
        for company in self.companies:
            company["data"] = get_day_yf_data(company["name"], date = self.date)
            #company["current_price"] = round(company["data"].iloc[self.timestep]["Open"], 2)
            #print(f"Current price for {company["name"]}: {company["current_price"]}\n")
        
    def _step_companies(self):
        self.companies = self.config.companies
        
        for company in self.companies:
            company["current_price"] = round(company["data"].iloc[self.timestep]["Open"], 2)
            print(f"Current price for {company["name"]}: {company["current_price"]}\n")
        
    
    def _initialize_variables(self):
        obs = []
        self.timestep = 0
        self.plot_created = False
        self.done = False
        self._load_config("config.json")
        self._initialize_companies()
        
        self._initialize_fig()
        return obs
        
    def reset(self):
        obs = self._initialize_variables()
        self.dataAdquisition.reset(self)
        print("Reseting...")
        
        # initialize Current_price and last_price
        if self.dataAdquisition.mode == "yfinance":
            keys = [key for key, value in self.dataAdquisition.get_current_data().items()]
            close = [value["Close"] for key, value in self.dataAdquisition.get_current_data().items()]
            # Suponiendo que keys es una lista de claves y close es una lista de valores
            self.current_price = dict(zip(keys, close))

            self.last_price = self.current_price
        
        
        return obs, False
    
    def step(self, action):
        # next_obs = []
        
        next_obs, done = self.dataAdquisition.step()
        #reward = {}
        total_reward = 0
        self.dataAdquisition.step()
        
        
        current_price = []
        #for company in self.companies:
            #current_price[company] = self.
        
        # Obtener el precio actual del activo y la fecha
        if self.dataAdquisition.mode == "offline":
            self.current_price = self.dataAdquisition.get_current_data()["Close"]
        elif self.dataAdquisition.mode == "yfinance":
            
            keys = [key for key, value in self.dataAdquisition.get_current_data().items()]
            close = [value["Close"] for key, value in self.dataAdquisition.get_current_data().items()]
            
            # Suponiendo que keys es una lista de claves y close es una lista de valores
            self.current_price = dict(zip(keys, close))
            # self.current_price = {key: {key: value} for key, value in zip(keys, close)}

            
            #self.current_price = self.dataAdquisition.get_current_data()["Close"]
        
        self.date = self.dataAdquisition.get_date()
        
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
            if len(self.portfolio.shares) > 0:
                # self.portfolio.capital += self.current_price

                if self.portfolio.sell_share(self): # Debería hacer lo de dentro
                    reward = self.current_price
                else:
                    action = 0
            else:
                print(f"No puedes vender por que no tienes acciones de la empresa {self.name}")
                print("Se pasa a Hold")
                action = 0
                reward = 0
        #else:  # HOLD
            
        # Update last price
        # self.last_price = self.current_price
        
        ############################################
        ############### TO DO !!!!!!!! #############
        #Step for companies
        # self._step_companies()
        
        self.timestep += 1
        if self.timestep > 100:
            done = True
        return next_obs, total_reward, reward, done, action
    
    def update_last_price(self):
        # Update last price
        self.last_price = self.current_price
    
    def render_old(self):
        current_data = self.dataAdquisition.get_current_data()
        if current_data is not None:
            #print("Estado actual del mercado:")
            # print(current_data)
            df = current_data
            df["High"].plot(), df["Low"].plot()
        else:
            print("No hay datos disponibles para renderizar en el mercado.")
            
    def _initialize_fig(self):
        # Si el gráfico no ha sido creado todavía, crearlo y mostrar el primer punto
        if self.render_mode == 'Individual':
            self.fig = plt.figure()
            self.ax = self.fig.add_subplot(211)
            self.ax.set_title("Estado actual del mercado")
            self.ax.set_xlabel("Paso")
            self.ax.set_ylabel("Precio")
            self.ax.grid()
            self.plot_created = True
        elif self.render_mode == 'MultiCompany':
            # self.fig = plt.figure()
            columns = len(self.companies)
            self.fig, self.axes = plt.subplots(columns, 1, figsize=(8, columns*4))
            
            
            
    def render_individual_company(self, action):
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
            
            # En un futuro quiero cambiar el plot por un gráfico de velas.
        else:
            print("No hay datos disponibles para renderizar en el mercado.")

    def render_multiCompany(self, actions):
        if self.dataAdquisition.mode == "offline":
            current_data = self.dataAdquisition.get_current_data()["Close"]
        elif self.dataAdquisition.mode == "yfinance":
            #current_data = self.dataAdquisition.get_current_data()["Close"]
            keys = [key for key, value in self.dataAdquisition.get_current_data().items()]
            close = [value["Close"] for key, value in self.dataAdquisition.get_current_data().items()]
            
            # Suponiendo que keys es una lista de claves y close es una lista de valores
            current_data = dict(zip(keys, close))
            # current_data = {key: {key: value} for key, value in zip(keys, close)}

            if not self.plot_created:
                self.plot_created = True
                
            
            
            # Obtén el color y la acción correspondiente
            color = self.COLORS[actions[0]]
            action_label = self.ACTIONS[actions[0]]
            # Obtén el color y la acción correspondiente
            color = self.COLORS[actions[0]]
            action_label = self.ACTIONS[actions[0]]
            
            # Legenda de colores
            legend_labels = [f"{self.COLORS[color]} = {self.ACTIONS[color]}" for color in self.COLORS]
        
        if self.dataAdquisition.mode == "offline":
            # print("Rendering..." + str(self.timestep) + " and data: " + str(current_data))
            if current_data is not None:
                
                columns = len(self.companies)

                # df del día de hoy:
                
                # Si el gráfico ya fue creado, simplemente añadir un punto al gráfico existente
                #self.ax.plot(self.timestep, current_data, color + 'o', label=action_label)
                for idx, column in enumerate(self.companies):
                    self.axes[idx].plot(self.timestep, current_data, color + 'o', label=action_label)
                    # self.axes[idx].legend(list(self.ACTIONS.values()))
                    self.axes[idx].legend(self.initial_date)
                    #self.axes[idx].set_ylabel(column)
                    
                    plt.pause(0.01)  # Pausa para actualizar el gráfico
                
                # En un futuro quiero cambiar el plot por un gráfico de velas.
            else:
                print("No hay datos disponibles para renderizar en el mercado.")            
            pass

        elif self.dataAdquisition.mode == "yfinance":
            # print("Rendering..." + str(self.timestep) + " and data: " + str(current_data))
            if current_data is not None:

                columns = len(current_data)
                
                # df del día de hoy:
                
                # Si el gráfico ya fue creado, simplemente añadir un punto al gráfico existente
                #self.ax.plot(self.timestep, current_data, color + 'o', label=action_label)
                print("Plotting...")
                for idx, column in enumerate(current_data):
                    # Create each subplot
                    self.axes[idx].plot(current_data[column], 'o', label="test")
                    #self.axes[idx].plot(self.timestep, current_data[column], color + 'o', label=action_label)
                    # self.axes[idx].legend(column)
                    #self.axes[idx].legend(str(self.initial_date))
                    
                    # print("idx: ")
                    # print(idx)   
                    # print("\n")
                    # print("column: ")
                    # print(column)
                    # plt.pause(0.01)  # Pausa para actualizar el gráfico
                    plt.show(block=False)
                
                # En un futuro quiero cambiar el plot por un gráfico de velas.
            else:
                print("No hay datos disponibles para renderizar en el mercado.")            
            pass

                
                
    def render(self, action):
        if self.render_mode == 'Individual':
            self.render_individual_company(action)
        elif self.render_mode == 'MultiCompany':
            self.render_multiCompany(action)
        else:
            assert "Wrong render mode selected"
