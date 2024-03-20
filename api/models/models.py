from sqlalchemy import  Column, Integer, String
from .database import Base


class AirQuality(Base):
    __tablename__ = "air_quality"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(String, index=True)
    longitude = Column(String, index=True)
    elevation = Column(String, index=True)
    type_gas = Column(String, index=True)
    data = Column(String, index=True)
    tag = Column(String, index=True)
    
    
