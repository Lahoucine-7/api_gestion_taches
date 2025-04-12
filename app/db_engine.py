# app/db_engine.py

from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///tasks.db"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},  # Utile pour SQLite en mode multithreadé
)
