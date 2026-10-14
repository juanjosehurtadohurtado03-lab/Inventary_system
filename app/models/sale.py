from sqlalchemy import Column, String, Integer, Boolean
from app.database.base import Base
from sqlalchemy.orm import relationship

class SaleModel(Base):
    __tablename__ = 'sales'
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String(10), nullable=False)
    time = Column(String(5), nullable=False)
    total = Column(Integer, nullable=False)
    is_active = Column(String(20), default='PENDIENTE')
    sale_details = relationship('SaleDetailsModel', back_populates='sale', cascade='all, delete-orphan')