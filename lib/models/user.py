from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from . import Base, get_session

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    is_admin = Column(Boolean, default=False)
    
    # Relationships
    dealerships = relationship("Dealership", back_populates="admin")
    purchases = relationship("Sale", back_populates="customer")
    
    @property
    def full_info(self):
        """Return formatted user information"""
        role = "Admin" if self.is_admin else "Customer"
        return f"User: {self.username} ({self.email}) - {role}"
    
    @classmethod
    def create(cls, username, email, password, is_admin=False):
        """Create a new user"""
        session = get_session()
        try:
            user = cls(username=username, email=email, password=password, is_admin=is_admin)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @classmethod
    def get_all(cls):
        """Get all users"""
        session = get_session()
        try:
            return session.query(cls).all()
        finally:
            session.close()