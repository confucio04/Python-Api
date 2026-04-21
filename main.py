from fastapi import FastAPI
from database import create_db_and_tables
from routers.estudiante_router import router as estudianter_router

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(estudianter_router)