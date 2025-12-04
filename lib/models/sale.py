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
    
    @property
    def sale_summary(self):
        """Return sale summary"""
        return f"Sale #{self.id}: {self.customer.username} bought {self.car.brand} {self.car.model} for ${self.sale_price:,.2f}"
    
    @classmethod
    def create(cls, customer_id, car_id, dealership_id, sale_price):
        """Create a new sale"""
        session = get_session()
        try:
            sale = cls(customer_id=customer_id, car_id=car_id, 
                      dealership_id=dealership_id, sale_price=sale_price)
            session.add(sale)
            session.commit()
            session.refresh(sale)
            return sale
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()