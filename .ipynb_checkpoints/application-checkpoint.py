#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 12:11:11 2023

@author: pablo
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func
from sqlalchemy.orm import Session

from pydantic import BaseModel


app = FastAPI()

# Configura la conexión a la base de datos MySQL
DATABASE_URL = "mysql+mysqlconnector://root:patacon@localhost/streaming_mysql"
engine = create_engine(DATABASE_URL)

# Define la tabla de datos en SQLAlchemy
Base = declarative_base()

class Movie(Base):
    __tablename__ = "tableA"

    show_id = Column(String(length=10), primary_key=True, index=True)
    
    title = Column(String(length=10000), index=True)
    cast = Column(String(length=10000), index=True)

    country = Column(String(length=10000), index=True)
    
    platform = Column(String(length=20), index=True)
    show_type = Column(String(length=10), index=True)
    release_year = Column(Integer, index=True)
    rating = Column(String(length=10), index=True)
    duration_int = Column(Integer, index = True)

# Crea la tabla si no existe
Base.metadata.create_all(bind=engine)

# Define un objeto Session para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def getDatabase():
    db = SessionLocal()
    try:    
        yield db
    finally:
        db.close()

@app.get("/count/{platform}")
def get_count_platform(platform: str, db: Session = Depends(getDatabase)):

    """Cantidad de películas (sólo películas, no series, etc) según plataforma. 
    La función debe llamarse get_count_platform(platform) y debe devolver un 
    int, con el número total de películas de esa plataforma. Las plataformas 
    deben llamarse amazon, netflix, hulu, disney."""

    count = db.query(Movie).filter(Movie.platform == platform, Movie.show_type == 'movie').count()
    return {"count": count}



@app.get("/content/{tipo}/{pais}/{anio}")
def prod_per_county(tipo: str, pais: str, anio: int, db: Session = Depends(getDatabase)):
    '''La cantidad de contenidos/productos (todo lo disponible en streaming) que 
    se publicó por país y año. La función debe llamarse prod_per_county(tipo,pais,
    anio) debería devolver la cantidad de contenidos/productos según el tipo de 
    contenido (pelicula, serie) por país y año en un diccionario con las variables 
    llamadas 'pais' (nombre del pais), 'anio' (año), 'cantidad' (cantidad de 
    contenidos/productos).'''

    contentCount = db.query(Movie).filter(
        Movie.show_type == tipo,
        Movie.country == pais,
        Movie.release_year == anio
    ).count()
    result = {'pais': pais, 'anio': anio, 'cantidad': contentCount}
    return result





@app.get("/rating/{rating}")
def get_contents(rating: str, db: Session = Depends(getDatabase)):
    '''La cantidad total de contenidos/productos (todo lo disponible en 
    streaming, series, peliculas, etc) según el rating de audiencia dado (para 
    qué público fue clasificada la película). La función debe llamarse 
    get_contents(rating) y debe devolver el numero total de contenido con ese 
    rating de audiencia.'''

    count = db.query(Movie).filter(Movie.rating == rating).count()
    return {'rating': rating, 'content_count': count}

# Define un modelo Pydantic para recibir los datos de salida
class MostCommonActorResponse(BaseModel):
    most_common_actor: str
    count: int

@app.get("/most_common_actor/{year}", response_model=MostCommonActorResponse)
def get_most_common_actor_by_year(year: int, db: Session = Depends(getDatabase)):
    """El actor más repetido en un año determinado"""

    result = (
        db.query(Movie.cast, func.count(Movie.cast).label("count"))
        .filter(Movie.release_year == year)  # Filtra por el año especificado
        .filter(Movie.cast != "")  # Excluye campos vacíos
        .filter(Movie.cast.isnot(None))  # Excluye campos nulos
        .group_by(Movie.cast)
        .order_by(func.count(Movie.cast).desc())
        .first()
    )
    return {"most_common_actor": result[0], "count": result[1]}




