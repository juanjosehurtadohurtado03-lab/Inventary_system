from sqlalchemy import Column, String, Integer, Boolean
from app.database.base import Base
from sqlalchemy.orm import relationship

class ProductModel(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    price = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)