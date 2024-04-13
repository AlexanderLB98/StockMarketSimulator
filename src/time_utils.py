import datetime
from datetime import datetime, timedelta

def change_format(cad: str) -> str:
    date = datetime.datetime.strptime(cad, "%Y-%m-%d").strftime("%d-%m-%Y")
    date_split = date.split("-")
    
    return "-".join([d.lstrip("0") for d in date_split])

def str_to_date(date_str: str) -> datetime:
    return datetime.datetime.strptime(date_str, '%Y-%m-%d')


# Para obtener la fecha de cualquier dia
def getDate(date: str): # '%Y-%m-%d'

    # Convertir la cadena de fecha actual a un objeto de fecha
    current_date_obj = datetime.strptime(date, '%Y-%m-%d')

    # Restar un día para obtener la fecha de ayer
    yesterday_date_obj = current_date_obj - timedelta(days=1)

    # Convertir la fecha de ayer de nuevo a una cadena en el formato deseado
    return yesterday_date_obj.strftime('%Y-%m-%d')
