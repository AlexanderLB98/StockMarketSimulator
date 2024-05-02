import matplotlib.pyplot as plt

from src.render.Render import Render

class RenderFigures(Render):
    
    # Define los colores y las acciones como variables de clase
    COLORS = {0: 'k',  # Negro para HOLD
              1: 'g',  # Verde para BUY
              2: 'r'}  # Rojo para SELL

    ACTIONS = {0: 'HOLD',
               1: 'BUY',
               2: 'SELL'}
    
    
    def __init__(self):
        super().__init__()  # Llama al método __init__ de la clase base
       
       
    def reset(self):
        self._initialize_fig()
        
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

