from pydantic import BaseModel

class AirQualitySchema(BaseModel):
    latitude: float
    longitude: float
    elevation: float
    type_gas: str
    tag: str
    data: list
