# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.settings import settings  # <- aqui o nome correto do arquivo

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL  # <- usa a variável de settings

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
