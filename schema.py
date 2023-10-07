#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@pabloPerez
perico3372@gmail.com

"""

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


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
    duration_int = Column(Integer, index=True)

# Crea la tabla si no existe
Base.metadata.create_all(bind=engine)
