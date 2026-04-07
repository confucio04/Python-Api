from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi import FastAPI
from pydantic import BaseModel
from sqlmodel import Field, SQLModel, create_engine, Session, select
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class EstudianteModelo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length= 30)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    email: str | None = None
    full_name: str | None 
    disabled: bool | None 

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user

@app.post("/estudiantes/")
def read_root(
    estudiante: EstudianteModelo, session: SessionDep,
     token: Annotated[str, Depends(oauth2_scheme)]
    ) -> EstudianteModelo:
    estudiante = session.exec(select(EstudianteModelo)).all()
    session.add(estudiante)
    session.commit()
    session.refresh(estudiante)
    return estudiante

@app.get("/estudiantes")
def read_root(session: SessionDep):
    estudiantes = session.exec(select(EstudianteModelo)).all() 
    return estudiantes

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}