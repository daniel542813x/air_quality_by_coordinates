from pydantic import BaseModel

"""Schema for the AirQuality model, used to validate on store 
   in the database.
"""
class AirQualitySchema(BaseModel):
    latitude: float
    longitude: float
    elevation: float
    type_gas: str
    tag: str
    data: list
