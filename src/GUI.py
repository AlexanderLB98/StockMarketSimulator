import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class StockSimulatorGUI:
    def __init__(self, root, market, broker):
        self.root = root
        self.market = market
        self.broker = broker
        
        self.root.title("Stock Simulator")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Crear un contenedor para el gráfico
        self.graph_frame = ttk.Frame(self.root)
        self.graph_frame.pack(pady=10)
        
        # Crear un lienzo para el gráfico
        self.figure = plt.Figure(figsize=(8, 6))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Botón para actualizar el gráfico
        self.update_button = ttk.Button(self.root, text="Actualizar Gráfico", command=self.update_graph)
        self.update_button.pack(pady=10)
        
    def update_graph(self):
        # Obtener datos del mercado y actualizar el gráfico
        market_data = self.market.get_data()
        prices = [data['price'] for data in market_data]
        dates = [data['date'] for data in market_data]
        
        self.ax.clear()
        self.ax.plot(dates, prices)
        self.ax.set_title("Precio de la Acción en el Tiempo")
        self.ax.set_xlabel("Fecha")
        self.ax.set_ylabel("Precio")
        self.canvas.draw()
        