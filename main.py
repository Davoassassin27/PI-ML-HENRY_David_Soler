from fastapi import FastAPI
import uvicorn
import pandas as pd
import numpy as np
import ast
from datetime import datetime
import locale
from sklearn.metrics.pairwise import cosine_similarity
import sklearn 

app = FastAPI()
# @app.get("/")
# def index():
#     return "Hola! Esta es una API de recomendación de peliculas. Para acceder a las consultas escriba en el link /Docs"
# http://127.0.0.1:8000
@app.get("/")
async def root():
    return {"message": "Hola! Esta es una API de recomendación de peliculas. Para acceder a las consultas escriba al final del link '/docs' H-API Coding! No olvidar respetar en las consultas La primera letra con mayuscula, por ejemplo, lunes => Lunes"}
df = pd.read_csv("dataset/dataset_cleaned.csv",low_memory=False)
data = pd.read_csv('dataset/dataset_ML.csv', low_memory=False) 
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

@app.get('/recomendacion/{titulo}')
def recomendacion(titulo:str):
    top_n = 5
    n = 2000
    data_subset = data.head(n)
    X = data_subset[['belongs_to_collection', 'genres', 'original_language', "popularity", "production_companies", "release_date", "runtime", "status", "vote_average", "return"]]  
    similarity_matrix = cosine_similarity(X)
    movie_index = data[data['title'] == titulo].index[0] 
    movie_similarities = similarity_matrix[movie_index]
    top_indices = movie_similarities.argsort()[-top_n-1:-1][::-1]  
    recommendations = df.loc[top_indices,"title"]
    return {'lista recomendada': str(recommendations.tolist())}