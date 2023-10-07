from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from pydantic import BaseModel
from sqlalchemy import Column, String, Integer

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from pydantic import BaseModel

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
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

    # Define las columnas de la tabla según tu base de datos
    show_id = Column(String(length=10), primary_key=True, index=True)
    title = Column(String(length=10000), index=True)
    cast = Column(String(length=1000), index=True)  # Agrega la columna cast aquí
    platform = Column(String(length=20), index=True)
    show_type = Column(String(length=10), index=True)
    release_year = Column(Integer, index=True)
    rating = Column(String(length=10), index=True)
    duration_int = Column(Integer, index=True)

# Crea una sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define un modelo Pydantic para recibir los datos de salida
class MostCommonActorResponse(BaseModel):
    most_common_actor: str
    count: int

@app.get("/most_common_actor/{year}")

def most_common_actor_by_year(
    year: int,
    # Agrega aquí el parámetro local_kw
    db: Session = Depends(SessionLocal)
):
    result = (
        db.query(Movie.cast, func.count(Movie.cast).label("count"))
        .filter(Movie.release_year == year)  # Filtra por el año especificado
        .filter(Movie.cast != "")  # Excluye campos vacíos
        .filter(Movie.cast.isnot(None))  # Excluye campos nulos
        .group_by(Movie.cast)
        .order_by(func.count(Movie.cast).desc())
        .first()
    )
    movie_count = db.query(Movie).filter(Movie.release_year == year).count()  # Obtiene la cantidad de películas
    return {
        "most_common_actor": result[0],
        "count": result[1],
        "movie_count": movie_count,
        
    }