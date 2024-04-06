
class option():
    def __init__(self, name, price, expiration_date):
        self.name = name                    # Nombre de la opción
        self.price = price                  # Precio actual de la opción
        self.expiration_date = expiration_date   # Fecha de vencimiento de la opción

    def update_price(self, new_price):
        self.price = new_price            # Método para actualizar el precio de la opción
        