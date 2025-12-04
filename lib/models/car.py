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
    
    @property
    def full_description(self):
        """Return full car description with status"""
        status = "SOLD" if self.is_sold else "AVAILABLE"
        return f"{self.year} {self.brand} {self.model} - {self.color} - ${self.price:,.2f} [{status}]"
    
    @property
    def is_available(self):
        """Check if car is available for purchase"""
        return not self.is_sold
    
    @classmethod
    def create(cls, brand, model, year, price, color, dealership_id):
        """Create a new car"""
        session = get_session()
        try:
            car = cls(brand=brand, model=model, year=year, price=price, 
                     color=color, dealership_id=dealership_id)
            session.add(car)
            session.commit()
            session.refresh(car)
            return car
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @classmethod
    def get_all(cls):
        """Get all cars"""
        session = get_session()
        try:
            return session.query(cls).all()
        finally:
            session.close()
    
    @classmethod
    def get_available(cls):
        """Get all available cars"""
        session = get_session()
        try:
            return session.query(cls).filter(cls.is_sold == False).all()
        finally:
            session.close()
    
    @classmethod
    def find_by_id(cls, car_id):
        """Find car by ID"""
        session = get_session()
        try:
            return session.query(cls).filter(cls.id == car_id).first()
        finally:
            session.close()
    
    @classmethod
    def find_by_brand(cls, brand):
        """Find cars by brand"""
        session = get_session()
        try:
            return session.query(cls).filter(cls.brand.ilike(f"%{brand}%")).all()
        finally:
            session.close()
    
    def mark_sold(self):
        """Mark car as sold"""
        session = get_session()
        try:
            self.is_sold = True
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def delete(self):
        """Delete this car"""
        session = get_session()
        try:
            session.delete(self)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()