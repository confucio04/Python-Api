# database.py
from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, create_engine, SQLModel

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# 1. Creamos el engine aquí
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

# 2. Definimos el generador de sesión aquí mismo
def get_session():
    with Session(engine) as session:
        yield session

# 3. Definimos SessionDep aquí
SessionDep = Annotated[Session, Depends(get_session)]

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)