import pandas as pd
import numpy as np

import yfinance as yf

from src.time_utils import getDate

# from time_utils import change_format --> TODO: Pasar a clase
import datetime

def change_format(cad: str) -> str:
    date = datetime.datetime.strptime(cad, "%Y-%m-%d").strftime("%d-%m-%Y")
    date_split = date.split("-")
    
    return "-".join([d.lstrip("0") for d in date_split])

def str_to_date(date_str: str) -> datetime.datetime:
    return datetime.datetime.strptime(date_str, '%Y-%m-%d')


class DataAdquisition:
    def __init__(self, mode = "offline", start_index = None) -> None:
        self.mode = mode
        #self.current_index = start_index
        
        if self.mode == "offline":
            data_path = "data/AEX.csv"
            self.load_from_csv(data_path)
            
        if start_index is None: # Esto igual sobra, cambiarlo
            self.start_index = 10
        self.get_yf_data("")
        
    
    def reset(self, start_index=None):
        self.current_index = self.start_index
        if start_index is None:
            self.start_index = np.random.randint(len(self.data) - 10)
        else:
            self.start_index = start_index
    
    
    def step(self):
        # Si llegamos al final:
        if not self.current_index < len(self.data) - 1:
            # Hemos llegado al final
            return [], True
        
        if self.mode == "offline":
            obs = self.get_current_data()
            
        #print("Current DataAdquisition index: " + str(self.current_index))
        
        self.current_index += 1
        
        return obs, False
    
    

    def get_current_data(self):
        return self.data.iloc[self.current_index]
    
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
        return change_format(self.data["Date"][self.current_index])
    
    def get_yf_data(company: str = None, start_date: str = None, end_date: str = None):
        # Obtener datos históricos para el índice AEX para la fecha actual
        
        company = "^AEX"
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