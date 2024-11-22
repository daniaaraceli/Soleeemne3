# -*- coding: utf-8 -*-
import pandas as pd
import requests
import streamlit as st

def obtener_datos_api(api_url):
    """Función que realiza la petición a la API y devuelve un DataFrame."""
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data)
    else:
        st.error('Error al obtener los datos de la API')
        return None

  
# Llamar la función para obtener los datos
api_url = "https://restcountries.com/v3.1/all"
df = obtener_datos_api(api_url)
# Si hay datos, mostrar el DataFrame, mostrar dataframe con las columna seleccionadas, permitir filtrado y mostrar gráficos.

if df is not None:
    st.write(df.head())

# Selección de columnas relevantes
    df['Nombre'] = df['name'].apply(lambda x: x.get('common') if isinstance(x, dict) else None)
    df['Región'] = df['region']
    df['Población'] = df['population']
    df['Área (km²)'] = df['area']
    df['Fronteras'] = df['borders'].apply(lambda x: len(x) if isinstance(x, list) else 0)
    df['Idiomas Oficiales'] = df['languages'].apply(lambda x: len(x) if isinstance(x, dict) else 0)
    df['Zonas Horarias'] = df['timezones'].apply(lambda x: len(x) if isinstance(x, list) else 0)

    # Filtrar columnas seleccionadas
    columnas = ['Nombre', 'Región', 'Población', 'Área (km²)', 'Fronteras', 'Idiomas Oficiales', 'Zonas Horarias']
    df_cleaned = df[columnas]

    # Mostrar DataFrame con las columnas seleccionadas
    st.title("Interacción con los datos:")
    st.write("Mostrar datos originales:")
    st.dataframe(df_cleaned)

    st.header("Selecciona una columna del dataframe utilizando un menú desplegable")
    columnas = st.multiselect('Selecciona las columnas a visualizar', df_cleaned.columns.tolist(), default=df_cleaned.columns.tolist())
    df_seleccionado = df_cleaned[columnas]
    # Mostrar el DataFrame con las columnas seleccionadas
    st.write('Columna Selecionada:')
    st.write(df_seleccionado)
    st.write("Estadísticas de las columnas seleccionadas:")
    st.write("Media:",)
    st.write(df_seleccionado.mean(numeric_only=True))
    st.write("Mediana:",)
    st.write(df_seleccionado.mean(numeric_only=True))
    st.write("Desviación estándar:",)
    st.write(df_seleccionado.std(numeric_only=True))

import matplotlib.pyplot as plt

# Mostrar DataFrame con las columnas seleccionadas
st.title("Interacción con los datos:")
st.write("Mostrar datos originales:")
st.dataframe(df_cleaned)

# Selección de columna
st.header("Selecciona una columna del dataframe utilizando un menú desplegable")
st.write("Selecciona las columnas a visualizar:")
df_seleccionado = df_cleaned[st.multiselect('Selecciona las columnas a visualizar:', df_cleaned.columns.tolist(), default=df_cleaned.columns.tolist())]

# Mostrar el DataFrame con las columnas seleccionadas
st.write('Columna Seleccionada:')
st.write(df_seleccionado)

# Mostrar estadísticas de las columnas seleccionadas
st.write("Estadísticas de las columnas seleccionadas:")

# Media
st.write("Media:")
st.write(df_seleccionado.mean(numeric_only=True))  # Solo columnas numéricas

# Mediana
st.write("Mediana:")
st.write(df_seleccionado.median(numeric_only=True))  # Solo columnas numéricas

# Desviación estándar
st.write("Desviación estándar:")
st.write(df_seleccionado.std(numeric_only=True))  # Solo columnas numéricas

# Crear gráfico de dispersión entre dos columnas seleccionadas
st.header("Gráfico de dispersión")

# Selección de columnas numéricas para el gráfico de dispersión
x_col = st.selectbox("Selecciona la columna para el eje X:", df_seleccionado.select_dtypes(include=['float64', 'int64']).columns)
y_col = st.selectbox("Selecciona la columna para el eje Y:", df_seleccionado.select_dtypes(include=['float64', 'int64']).columns)

# Mostrar el gráfico de dispersión si se han seleccionado ambas columnas
if x_col and y_col:
    fig, ax = plt.subplots()
    ax.scatter(df_seleccionado[x_col], df_seleccionado[y_col])
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(f"Gráfico de {x_col} vs {y_col}")
    st.pyplot(fig)

# Crear gráfico de barras para una columna categórica
st.header("Gráfico de barras de una columna categórica")

# Selección de columna categórica para graficar
columna_categorica = st.selectbox("Selecciona la columna categórica para el gráfico de barras:", ['Región', 'Zonas Horarias'])

# Mostrar el gráfico de barras
if columna_categorica:
    fig, ax = plt.subplots()
    df_seleccionado[columna_categorica].value_counts().plot(kind='bar', ax=ax)
    ax.set_title(f"Distribución de {columna_categorica}")
    st.pyplot(fig)

