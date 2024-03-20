from aiohttp import WebSocketError
from utils import is_validate_air_quality_params
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
    """Read all air quality data from the database

    Returns:
        _type_: list of AirQuality
    """    
    return db.query(AirQuality).all()


@router.get("/store/api/data/{id}")
async def read_air_quality(id: int):
    """Read air quality data from the database by id

    Args:
        id (int): id of the air quality data

    Returns:
        _type_: AirQuality or None
    """    
    try:
        
        return db.query(AirQuality).filter(AirQuality.id == id).first()
    
    except Exception as e:
        print(str(e))
        return {
            'success': False,
            'code': 404,
        }


@router.get("/api/data")
async def get_air_quality(latitude: float, longitude: float, type_gas: str, forecast_days: int):
    """Get air quality data from the Open Mateo API.

    Args:
        latitude (float): Latitude of the location
        longitude (float): Longitude of the location
        type_gas (str): Type of gas, ('pm10', 'pm2.5', 'carbon_monoxide','nitrogen_dioxide','sulphur_dioxide')
        forecast_days (int): Number of days to forecast 16 > forecast_days > 0 

    Returns:
        _type_: dict
    """    
    try:

        if type_gas not in AVAILABLE_GASES:
            raise ValueError("Invalid gas type")
    
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": type_gas.lower(),
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
    except Exception as e:
        return {
            'success': False,
            'code': 404,
            'message': 'Invalid parameters or error in the Open Mateo API'
        }
    
@router.post("/api/data")
async def create_air_quality(air_quality: AirQualitySchema):
    """Create air quality data in the database

    Args:
        air_quality (AirQualitySchema): AirQualitySchema object

    Returns:
        _type_: number 
    """    
    try:
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

    except Exception as e:
        return {
            "error": str(e)
        }
    

@router.websocket("/sync/data")
async def websocket_endpoint(websocket: WebSocket):
    """Websocket endpoint to get air quality data from the Open Mateo API 

    Args:
        websocket (WebSocket): Websocket object with parameters latitude, longitude, type_gas, forecast
    """    
    await websocket.accept()
    try:
        while True:

            # Get data from the client
            data = await websocket.receive_json()
            
            if not is_validate_air_quality_params(data):
                raise ValueError("Invalid parameters")
            

            json_data = {
                "latitude": data["latitude"],
                "longitude": data["longitude"],
                "type_gas": data["type_gas"],
                "forecast_days": data["forecast_days"]
            }
            
            # Get air quality data from the Open Mateo API by get_air_quality function
            data = await get_air_quality(**json_data)
            
            await websocket.send_json(data)
    except Exception as e:
        print(str(e))
        await websocket.send_json({"error": "Invalid parameters"})
        await websocket.close()