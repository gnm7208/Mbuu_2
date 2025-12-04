from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from . import Base, get_session

class Car(Base):
    __tablename__ = 'cars'
    
    id = Column(Integer, primary_key=True)
    brand = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    color = Column(String(30), nullable=False)
    is_sold = Column(Boolean, default=False)
    dealership_id = Column(Integer, ForeignKey('dealerships.id'), nullable=False)
    
    # Relationships
    dealership = relationship("Dealership", back_populates="cars")
    sale = relationship("Sale", back_populates="car", uselist=False)