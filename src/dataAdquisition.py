import pandas as pd
import numpy as np

class DataAdquisition:
    def __init__(self, mode = "offline", start_index = None) -> None:
        self.mode = mode
        #self.current_index = start_index
        
        if self.mode == "offline":
            data_path = "data/AEX.csv"
            self.load_from_csv(data_path)
            
        if start_index is None: # Esto igual sobra, cambiarlo
            self.start_index = 10
        
    
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
            
    