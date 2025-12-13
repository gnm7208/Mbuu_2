# models/car_image.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import Base, get_session

class CarImage(Base):
    __tablename__ = "car_images"
    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)
    url = Column(String(300), nullable=False)
    is_main = Column(Boolean, default=False)

    car = relationship("Car", back_populates="images")
