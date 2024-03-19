from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


# class for store latitude,longitude,elevation,type, diccionary of the data
class AirQuality(Base):
    __tablename__ = "air_quality"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(String, index=True)
    longitude = Column(String, index=True)
    elevation = Column(String, index=True)
    type = Column(String, index=True)
    data = Column(String, index=True)
    tags = Column(String, index=True)
    
    
