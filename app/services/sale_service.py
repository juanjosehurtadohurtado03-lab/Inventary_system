import sqlite3 
from app.repositories.sale_repository import CRUD_sale
from app.schemas.sale import SaleData, SaleCreate
from app.services.products_service import ProductServices
from fastapi import HTTPException, status

class SaleService:
    def __init__(self, repo: CRUD_sale, ProductService: ProductServices):
        self.repo = repo
        self.ProductService = ProductService
    
    def verific_and_add_product_sale(self, sale_data: SaleCreate):
        total = 0
        processed_item = []
        
        try:
            for item in sale_data.items:
                if item.id or item.name:
                    product = self.ProductService.search_product_verific(item.id, item.name)
                    if product is None:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'El producto {item.name or item.id} no existe en el inventario..'
                        )
                    if product.stock < item.quantity:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No contamos con {item.quantity} unidades de {product.name} en el inventario.'
                        )
                    total += (product.price * item.quantity)
                    update_stock = product.stock - item.quantity
                    self.ProductService.update_stock_by_id(product.id, update_stock)
                    
                    processed_item.append({
                        'product_id': product.id,
                        'name': product.name,
                        'quantity': item.quantity,
                        'price_unit': product.price,
                        'subtotal': product.price * item.quantity
                    })
                else:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail='No se permiten campos vacios.'
                    )
        
            return self.repo.create_sale(ci_client=sale_data.ci_customer, total=total, sale_details=processed_item)
        except sqlite3.Error as e:
            self.repo.db.rollback()
            raise HTTPException(
                status_code=404, detail=f'SQL error: {e}'
            )