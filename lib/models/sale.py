from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from . import Base, get_session

class Sale(Base):
    __tablename__ = 'sales'
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    car_id = Column(Integer, ForeignKey('cars.id'), nullable=False)
    dealership_id = Column(Integer, ForeignKey('dealerships.id'), nullable=False)
    sale_price = Column(Float, nullable=False)
    sale_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    customer = relationship("User", back_populates="purchases")
    car = relationship("Car", back_populates="sale")
    dealership = relationship("Dealership", back_populates="sales")