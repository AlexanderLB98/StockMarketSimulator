import pandas as pd
import numpy as np

from random import randrange
from datetime import timedelta

import yfinance as yf

from src.Time_utils import getDate

# from time_utils import change_format --> TODO: Pasar a clase
import datetime

def change_format(cad: str) -> str:
    date = datetime.datetime.strptime(cad, "%Y-%m-%d").strftime("%d-%m-%Y")
    date_split = date.split("-")
    
    return "-".join([d.lstrip("0") for d in date_split])

def str_to_date(date_str: str) -> datetime.datetime:
    return datetime.datetime.strptime(date_str, '%Y-%m-%d')

def get_random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    
    start = datetime.datetime.strptime(start, "%d-%m-%Y")
    
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

class DataAdquisition:
    def __init__(self, mode = "offline", start_index = None) -> None:
        self.mode = mode
        self.current_index = start_index
        
        if self.mode == "offline":
            data_path = "data/AEX.csv"
            self.load_from_csv(data_path)
        if self.mode == 'yfinance':
            """
            Aqui necesitaré la lista de compañías del mercado, como la fecha inicial.
            Dare una fecha inicial, y se generará un día aleatorio entre dicha fecha
            y la fecha actual. Ese será el primer día. Será el mismo para todas las 
            compañías, obviamente.
            """
            print("Setting yfinance mode...")
            self.data = {}
            self.current_data = {}
            
        if start_index is None: # Esto igual sobra, cambiarlo
            self.start_index = 10
        #self.get_yf_data("")
        
    
    def reset(self, market, start_index=None):
          
        if self.mode == 'offline':
            self.current_index = self.start_index
            if start_index is None:
                self.start_index = np.random.randint(len(self.data) - 10)
            else:
                self.start_index = start_index
                
        elif self.mode == 'yfinance':
            
            # Inicializar las compañías
            self.companies = market.companies
            self.current_data = {}
            # Genero una fecha aleatoria entre la fecha dada y la actual
            start_date = market.initial_date 
            end_date = datetime.datetime.today()
            
            initial_date = get_random_date(start=start_date, end = end_date)
            market.initial_date = initial_date
            
            print(initial_date)
    
            # Por modificar a la fecha generada arriba
            self.start_index = market.initial_date # Must set initial date in market
            self.current_index = self.start_index #datetime
            
            print("2")
            self.data = {}
            # Fetch data from that date to today for every company
            for company in self.companies:
                self.data[company["name"]] = get_yf_data(company["name"],self.current_index, datetime.datetime.today())
                print(self.data[company["name"]])
    
    def step(self):
        # Si llegamos al final:
        if self.mode == "offline":
            if not self.current_index < len(self.data) - 1:
                # Hemos llegado al final
                return [], True
        elif self.mode == "yfinance":
            if not self.current_index < self.data[self.companies[0]["name"]].index[-1]:
                # Hemos llegado al final
                return [], True
        
        if self.mode == "offline":
            obs = self.get_current_data()
            
        if self.mode == "yfinance":
            obs = self.get_current_data_companies(self.current_index)
        #print("Current DataAdquisition index: " + str(self.current_index))
        
        self.current_index += timedelta(days=1)
        
        #self.current_index += 1
        
        return obs, False
    
    
    def get_current_data_companies(self, date) -> dict: 
        """_summary_
            returns dict with 
                key: "name"
                value: data for current day
        Returns:
            dict: _description_
        """
        print("x")
        #data_companies = []
        for company in self.companies:
            # Incluir un trycatch por si no encuentra datos para ese día --> TODO!
            try:
                data_company = self.data[company["name"]].loc[date]
            except KeyError as e:
                print("Key error, filtering data by date: " + str(date.strftime("%d-%m-%Y")))
                data_company = {}
            self.current_data[company["name"]] = data_company
        
        #return data_companies
        return self.current_data

    def get_current_data(self):
        
        if self.mode == "offline":
            return self.data.iloc[self.current_index]
        elif self.mode == "yfinance":
            # data = {}
            for company, company_data in self.data.items():
                current_date = self.current_index
                # data =  
                self.current_data[company] = self.data[company].loc[datetime.datetime.strptime("2024-01-19", "%Y-%m-%d")]
            return self.current_data
        else:
            assert "modo incorrecto seleccionado en DataAdquisiton"
    
    def load_from_csv(self, data_path):
        try:
            df = pd.read_csv(data_path)
            self.data = df
        except Exception as e:
            print("Error: " + str(e))
            
        return df
    
    def get_start_date(self):
        return change_format(self.data["Date"][self.start_index])
    
    def get_date(self):
        if self.mode == "offline":
            return change_format(self.data["Date"][self.current_index])
        elif self.mode == "yfinance":
            pass
        
        
    def get_yf_data(company, start_date, end_date):
        # Obtener datos históricos para el índice AEX para la fecha actual
        
        #company = company
        start_date = start_date or getDate("2020-01-10")
        start_date = start_date or getDate("2021-12-31")
        
        data = yf.download(company, start=start_date, end=end_date)

        # Verificar si se obtuvieron datos para el día actual
        if not data.empty:
            # Mostrar los datos más importantes
            first_data = data.iloc[0]
            result = {
                "Compañia": f'AEX --> ({start_date} -> {end_date}):',
                "Apertura": f': {round(first_data["Open"], 2)}€',
                "Máximo": f': {round(first_data["High"], 2)}€',
                "Mínimo": f': {round(first_data["Low"], 2)}€',
                "Cierre": f': {round(first_data["Close"], 2)}€',
                "Volumen": f': {int(first_data["Volume"])}',
            }
            print(result)
            last_data = data.iloc[-1]
            result = {
                "Compañia": f'AEX --> ({start_date} -> {end_date}):',
                "Apertura": f': {round(last_data["Open"], 2)}€',
                "Máximo": f': {round(last_data["High"], 2)}€',
                "Mínimo": f': {round(last_data["Low"], 2)}€',
                "Cierre": f': {round(last_data["Close"], 2)}€',
                "Volumen": f': {int(last_data["Volume"])}',
            }
            print(result)
            return data
        else:
            result = 'No hay datos disponibles.'
            assert "No Data from yfinance"
        pass
    
    def get_day_yf_data(company: str = None, date: str = None):
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
    
    
    """_summary_
    Metodo para sacar datos del df companies
    """
    def get_current_price():
        pass
    
    
def get_yf_data(company, start_date, end_date):
    # Obtener datos históricos para el índice AEX para la fecha actual
    
    #company = company
    start_date = start_date or getDate("2020-01-10")
    start_date = start_date or getDate("2021-12-31")
    
    data = yf.download(company, start=start_date, end=end_date)

    # Verificar si se obtuvieron datos para el día actual
    if not data.empty:
        # Mostrar los datos más importantes
        first_data = data.iloc[0]
        result = {
            "Compañia": f'AEX --> ({start_date} -> {end_date}):',
            "Apertura": f': {round(first_data["Open"], 2)}€',
            "Máximo": f': {round(first_data["High"], 2)}€',
            "Mínimo": f': {round(first_data["Low"], 2)}€',
            "Cierre": f': {round(first_data["Close"], 2)}€',
            "Volumen": f': {int(first_data["Volume"])}',
        }
        print(result)
        last_data = data.iloc[-1]
        result = {
            "Compañia": f'AEX --> ({start_date} -> {end_date}):',
            "Apertura": f': {round(last_data["Open"], 2)}€',
            "Máximo": f': {round(last_data["High"], 2)}€',
            "Mínimo": f': {round(last_data["Low"], 2)}€',
            "Cierre": f': {round(last_data["Close"], 2)}€',
            "Volumen": f': {int(last_data["Volume"])}',
        }
        print(result)
        return data
    else:
        result = 'No hay datos disponibles.'
        assert "No Data from yfinance"
    pass