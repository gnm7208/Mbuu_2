from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import Base, get_session

class Dealership(Base):
    __tablename__ = 'dealerships'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    location = Column(String(200), nullable=False)
    admin_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    image_url = Column(String(300), nullable=True)
    
    # Relationships
    admin = relationship("User", back_populates="dealerships")
    cars = relationship("Car", back_populates="dealership", cascade="all, delete-orphan")
    sales = relationship("Sale", back_populates="dealership")
    
    @property
    def car_count(self):
        """Return number of cars in dealership"""
        session = get_session()
        try:
            from .car import Car
            return session.query(Car).filter(Car.dealership_id == self.id).count()
        finally:
            session.close()
    
    @property
    def total_sales(self):
        """Return total number of sales"""
        session = get_session()
        try:
            from .sale import Sale
            return session.query(Sale).filter(Sale.dealership_id == self.id).count()
        finally:
            session.close()
    
    @classmethod
    def create(cls, name, location, admin_id):
        """Create a new dealership"""
        session = get_session()
        try:
            dealership = cls(name=name, location=location, admin_id=admin_id)
            session.add(dealership)
            session.commit()
            session.refresh(dealership)
            return dealership
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @classmethod
    def get_all(cls):
        """Get all dealerships"""
        session = get_session()
        try:
            dealerships = session.query(cls).all()
            # Trigger lazy loading while session is open
            for dealership in dealerships:
                _ = dealership.admin.username
                _ = len(dealership.cars)
                _ = len(dealership.sales)
            return dealerships
        finally:
            session.close()
    
    @classmethod
    def find_by_id(cls, dealership_id):
        """Find dealership by ID"""
        session = get_session()
        try:
            return session.query(cls).filter(cls.id == dealership_id).first()
        finally:
            session.close()
    
    @classmethod
    def find_by_admin(cls, admin_id):
        """Find dealerships by admin ID"""
        session = get_session()
        try:
            dealerships = session.query(cls).filter(cls.admin_id == admin_id).all()
            # Trigger lazy loading while session is open
            for dealership in dealerships:
                _ = dealership.admin.username
                _ = len(dealership.cars)  # Load cars relationship
                _ = len(dealership.sales)  # Load sales relationship
            return dealerships
        finally:
            session.close()
    
    def delete(self):
        """Delete this dealership"""
        session = get_session()
        try:
            session.delete(self)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()