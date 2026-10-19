from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.product import ProductModel
from app.models.sale import SaleModel
from app.models.sale_details import SaleDetailsModel
from typing import Any

class CRUD_sale:
    def __init__(self, db: Session):
        self.db = db
    
    def create_sale(self, ci_client: int, total: int, sale_details: list[dict[str: Any]]):
        new_sale = SaleModel(
            ci_customer=ci_client,
            total=total
        )
        
        items_details_list = []
        for item in sale_details:
            detail = SaleDetailsModel(
                name=item['name'],
                quantity=item['quantity'],
                price_unit=item['price_unit'],
                subtotal=item['subtotal'],
                product_id=item['product_id']
            )
            items_details_list.append(detail)
        
        new_sale.sale_details = items_details_list
        
        self.db.add(new_sale)
        self.db.commit()
        self.db.refresh(new_sale)
        return new_sale