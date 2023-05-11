from fastapi import FastAPI
import uvicorn
import pandas as pd
import numpy as np
import ast
from datetime import datetime
import locale

app = FastAPI()
# http://127.0.0.1:8000
df = pd.read_csv("dataset/dataset_cleaned.csv",low_memory=False)

# @app.get("/")
# def index() :
#     return "Hola"
@app.get("/")
def index() :
    pass
@app.get('/peliculas_mes/{mes}')
def peliculas_mes(mes:str):
    aux = df.groupby("month_name").size()
    respuesta = aux [mes]

    return {'mes':mes, 'cantidad':str(respuesta)}

@app.get('/peliculas_dia/{dia}')
def peliculas_dia(dia:str):
    aux = df.groupby("day_name").size()
    respuesta = aux [dia]
    return {'dia':dia, 'cantidad':str(respuesta)}
@app.get('/franquicia/{franquicia}')
def franquicia(franquicia:str):
    aux = df.groupby("belongs_to_collection").size()
    cantidad = aux [franquicia]
    ganancia = df.query("belongs_to_collection == @franquicia")['revenue'].sum()
    promedio = df.query("belongs_to_collection == @franquicia")['revenue'].mean()
    return {'franquicia':franquicia, 'cantidad de peliculas':str(cantidad), 'ganancia_total':str(ganancia), 'ganancia_promedio':str(promedio)}

@app.get('/peliculas_pais/{pais}')
def peliculas_pais(pais:str):
    df["production_countries"] = df["production_countries"].fillna("")
    df_filtrado = df[df['production_countries'].apply(lambda x: pais in str(x))]
    cantidad_peliculas = len(df_filtrado)
    return {'pais':pais, 'cantidad':str(cantidad_peliculas)}

@app.get('/productoras/{productora}')
def productoras(productora:str):
    df_filtrado = df[df['production_companies'].apply(lambda x: productora in str(x))]
    cantidad = len(df_filtrado)
    ganancia= df_filtrado["revenue"].sum()
    return {'productora':productora, 'ganancia_total':str(ganancia), 'cantidad':str(cantidad)}

@app.get('/retorno/{pelicula}')
def retorno(pelicula:str):
    df_filtrado = df[df['title'].apply(lambda x: pelicula.strip() == str(x).strip())]
    inversion= df_filtrado["budget"].sum()
    ganancia= df_filtrado["revenue"].sum()
    retorno= df_filtrado["return"].sum()
    anio = pd.to_datetime(df_filtrado["release_date"]).dt.year
    return {'pelicula':pelicula, 'inversion':str(inversion), 'ganacia':str(ganancia),'retorno':str(retorno), 'anio':str(anio.item())}
# ML
# @app.get('/recomendacion/{titulo}')
# def recomendacion(titulo:str):
#     '''Ingresas un nombre de pelicula y te recomienda las similares en una lista'''
#     return {'lista recomendada': respuesta}