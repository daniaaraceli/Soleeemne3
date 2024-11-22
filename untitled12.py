# -*- coding: utf-8 -*-
import pandas as pd 
import requests

# Consulta a la API REST
url = "https://restcountries.com/v3.1/all"
response = requests.get(url)
response.raise_for_status() # Verifica que no haya errores en la consulta

# Extrae los datos directamente en un DataFrame
data = response.json()  # Los datos se descargan como lista de diccionarios
df = pd.DataFrame(data)  # Convertimos la lista a DataFrame
