from aiohttp import WebSocketError
from models.main import get_db
from fastapi import APIRouter,WebSocket
from enums import URL_OPEN_MATEO_API, AVAILABLE_GASES
from models import *
import requests
from models.schema import  AirQualitySchema

db = get_db()


router = APIRouter(
    prefix="/air_quality",
)


@router.get("/store/api/data")
async def read_root():
    return db.query(AirQuality).all()


@router.get("/store/api/data/{id}")
async def read_air_quality(id: int):
    return db.query(AirQuality).filter(AirQuality.id == id).first()


@router.get("/api/data")
async def get_air_quality(latitude: float, longitude: float, type_gas: str, forecast_days: int):
    
    if type_gas not in AVAILABLE_GASES:
        return {
            "error": "Invalid type of gas"
        }
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": type_gas,
        "forecast_days": forecast_days
    }
    
    response = requests.get(URL_OPEN_MATEO_API, params=params)
    
    data = response.json()
    
    result_by_hour = []
    
    for idx, hour in enumerate(data["hourly"]['time']):
        result_by_hour.append({
            "hour": hour,
            "value": data["hourly"][type_gas][idx]
        })
            
    return {
        "elevation": data["elevation"],
        "type_gas": type_gas,
        "latitude": latitude,
        "longitude": longitude,
        "forecast_days": forecast_days,
        "data": result_by_hour
    }
    
    
@router.post("/api/data")
async def create_air_quality(air_quality: AirQualitySchema):
    
    air_quality_obj = AirQuality(
        latitude=air_quality.latitude,
        longitude=air_quality.longitude,
        elevation=air_quality.elevation,
        type_gas=air_quality.type_gas,
        data=str(air_quality.data),
        tag=air_quality.tag 
    )
    
    db.add(air_quality_obj)
    db.commit()
    
    return {
        "message": "Data created successfully"
    }



@router.websocket("/communicate")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Connected")
    try:
        while True:
            print(websocket)
            data = await websocket.receive_json()

            json_data = {
                "latitude": data["latitude"],
                "longitude": data["longitude"],
                "type_gas": data["gas_type"],
                "forecast_days": data["forecast"]
            }
            
            data = await get_air_quality(**json_data)
            
            await websocket.send_json(data)
    except WebSocketError:
        print(str(WebSocketError))
