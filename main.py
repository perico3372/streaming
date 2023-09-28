#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 12:11:11 2023

@author: pablo
"""

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
from sqlalchemy.orm import Session

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
    """Cantidad de películas (sólo películas, no series, etc) según plataforma."""
    count = db.query(Movie).filter(Movie.platform == platform, Movie.show_type == 'movie').count()
    return {"count": count}
"""
@app.get("/content/{tipo}/{pais}/{anio}")
def prod_per_county(tipo: str, pais: str, anio: int, db: Session = Depends(getDatabase)):
    '''La cantidad de contenidos/productos (todo lo disponible en streaming) que 
    se publicó por país y año.'''
    contentCount = db.query(Movie).filter(
        Movie.show_type == tipo,
        Movie.platform == pais,
        Movie.release_year == anio
    ).count()
    result = {'pais': pais, 'anio': anio, 'tipo': contentCount}
    return result
"""


@app.get("/content/{tipo}/{pais}/{anio}")
def prod_per_county(tipo: str, pais: str, anio: int, db: Session = Depends(getDatabase)):
    '''La cantidad de contenidos/productos (todo lo disponible en streaming) que 
    se publicó por país y año.'''
    
    # Debugging: Print the values of tipo, pais, and anio.
    print(f"tipo: {tipo}, pais: {pais}, anio: {anio}")
    
    contentCount = db.query(Movie).filter(
        Movie.show_type == tipo,
        Movie.platform == pais,
        Movie.release_year == anio
    ).count()
    
    # Debugging: Print the generated SQL query.
    print(f"SQL Query: {str(db.query(Movie).filter(Movie.show_type == tipo, Movie.platform == pais, Movie.release_year == anio))}")
    
    result = {'pais': pais, 'anio': anio, 'tipo': contentCount}
    return result

@app.get("/rating/{rating}")
def get_contents(rating: str, db: Session = Depends(getDatabase)):
    '''La cantidad total de contenidos/productos según el rating de audiencia dado.'''
    count = db.query(Movie).filter(Movie.rating == rating).count()
    return {'rating': rating, 'content_count': count}

from typing import Union



