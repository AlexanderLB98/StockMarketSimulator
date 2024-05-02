import uvicorn

from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel
from typing import Optional

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from fastapi import Request
from fastapi.staticfiles import StaticFiles

from sim import sim

import plotly.graph_objs as go

# http://127.0.0.1:8000/
app = FastAPI()

# Cargar plantillas HTML
templates = Jinja2Templates(directory="templates")  # Asegúrate de que tu plantilla esté en un directorio llamado "templates"

# Configurar la ruta para servir archivos estáticos
app.mount("/web", StaticFiles(directory="web"), name="static")



@app.get("/", response_class=HTMLResponse)
async def read_menu(request: Request):
    # Renderiza la página de inicio (menu.html) utilizando la plantilla base
    return templates.TemplateResponse("inicio.html", {"request": request})

@app.get("/pagina1", response_class=HTMLResponse)
async def read_pagina1(request: Request):
    # Renderiza la página 1 (pagina1.html) utilizando la plantilla base
    return templates.TemplateResponse("pagina1.html", {"request": request})

@app.get("/pagina2", response_class=HTMLResponse)
async def read_pagina2(request: Request):
    # Renderiza la página 2 (pagina2.html) utilizando la plantilla base
    return templates.TemplateResponse("pagina2.html", {"request": request})

@app.get("/pagina3", response_class=HTMLResponse)
async def read_pagina3(request: Request):
    # Renderiza la página 3 (pagina3.html) utilizando la plantilla base
    return templates.TemplateResponse("pagina3.html", {"request": request})

@app.get("/pagina4", response_class=HTMLResponse)
async def read_pagina4(request: Request):
    # Renderiza la página 4 (pagina4.html) utilizando la plantilla base
    return templates.TemplateResponse("pagina4.html", {"request": request})





def extract_simulation_data(simulation_results):
    """
    Extrae los datos de simulación de una lista de resultados y los organiza en listas separadas.
    
    Args:
    - simulation_results: Lista de resultados de la simulación, donde cada elemento es un diccionario con datos de mercado.
    
    Returns:
    - Una tupla de listas que contienen los datos extraídos: (dates, opens, highs, lows, closes, adj_closes, volumes)
    """
    dates = []
    opens = []
    highs = []
    lows = []
    closes = []
    adj_closes = []
    volumes = []

    for item in simulation_results:
        dates.append(item['Date'])
        opens.append(item['Open'])
        highs.append(item['High'])
        lows.append(item['Low'])
        closes.append(item['Close'])
        adj_closes.append(item['Adj Close'])
        volumes.append(item['Volume'])

    return dates, opens, highs, lows, closes, adj_closes, volumes
 

def extract_simulation_data_dict(simulation_results):
    """
    Extrae los datos de simulación de una lista de resultados y los organiza en un diccionario.

    Args:
    - simulation_results: Lista de resultados de la simulación, donde cada elemento es un diccionario con datos de mercado.

    Returns:
    - Un diccionario con los datos extraídos, donde las claves son los nombres de las columnas y los valores son listas de datos correspondientes.
    """
    data_dict = {}

    # Iterar sobre los diccionarios en la lista
    for item in simulation_results:
        # Iterar sobre las claves en el diccionario
        for key, value in item.items():
            # Verificar si la clave ya está en el diccionario
            if key in data_dict:
                data_dict[key].append(value)
            else:
                # Si la clave no está en el diccionario, crear una nueva lista con el primer valor
                data_dict[key] = [value]

    return data_dict

# Funcion para enseñar una simulación.
# Ruta para la nueva página que muestra los resultados de la simulación
@app.get("/market_simulation", response_class=HTMLResponse)
async def market_simulation(request: Request):
    # Realiza la simulación y obtiene los resultados
    simulation_results = sim()
    
    sim_results = extract_simulation_data_dict(simulation_results)
    
    # Gráfica los resultados de la simulación
    dates = sim_results["Date"]
    close = sim_results["Close"]
    fig = go.Figure(data=[go.Bar(x=dates, y=close)])
    graph_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

    # Renderiza la plantilla HTML con los resultados de la simulación
    return templates.TemplateResponse("market_simulation.html", {"request": request, "graph_html": graph_html})




if __name__ == "__main__":
    # uvicorn.run(app, host="127.0.0.1", port=8000) # LocalHost
    uvicorn.run(app, host="0.0.0.0", port=8080)
    #uvicorn.run(app, host="255.255.240.0", port=8000)
    



