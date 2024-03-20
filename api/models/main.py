from fastapi import FastAPI
from .database import SessionLocal

app = FastAPI()


""" Get usable database session
"""
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()