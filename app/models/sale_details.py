from sqlalchemy import ForeignKey, Column, String, Integer, Boolean
from app.database.base import Base
from sqlalchemy.orm import relationship

class SaleDetailsModel(Base):
    __tablename__ = 'sale_details'
    
    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)
    sale_id = Column(Integer, ForeignKey('sales.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    sale = relationship('SaleModel', back_populates='sale_details')
    product = relationship('ProductModel', back_populates='product_details')