class share():
    def __init__(self, name, price, quantity):
        self.name = name           # Nombre de la acción
        self.price = price         # Precio actual de la acción
        self.quantity = quantity   # Cantidad de acciones disponibles

    def update_price(self, new_price):
        self.price = new_price     # Método para actualizar el precio de la acción
        
