from fastapi import FastAPI
from .database import SessionLocal, engine,Base

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()