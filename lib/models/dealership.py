from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import Base, get_session

class Dealership(Base):
    __tablename__ = 'dealerships'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    location = Column(String(200), nullable=False)
    admin_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Relationships
    admin = relationship("User", back_populates="dealerships")
    cars = relationship("Car", back_populates="dealership", cascade="all, delete-orphan")
    sales = relationship("Sale", back_populates="dealership")