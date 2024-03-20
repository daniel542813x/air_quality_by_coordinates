from pydantic import BaseModel

class AirQualitySchema(BaseModel):
    id: int
    latitude: str
    longitude: str
    elevation: str
    type_gas: str
    data: str
    tag: str
