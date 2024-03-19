
from models.main import get_db
from fastapi import APIRouter
from models import *

db = get_db()

router = APIRouter(
    prefix="/air_quality",
)

@router.get("/")
async def read_root():
    return db.query(AirQuality).all()
