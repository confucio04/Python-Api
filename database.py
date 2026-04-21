from typing import Annotated

from sqlmodel import SQLModel, create_engine
from fastapi import Depends
from sqlmodel import Session, create_engine, SQLModel

from dependencias import get_session

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

SessionDep = Annotated[Session, Depends(get_session)]

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)