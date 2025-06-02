from fastapi import FastAPI
from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)  # Cria tabelas no PostgreSQL

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API no ar!"}
