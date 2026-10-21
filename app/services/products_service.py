from app.schemas.product import ProductCreate

from fastapi import HTTPException, status
from app.repositories.product_repository import CRUD_products

class ProductServices:
    def __init__(self, repo: CRUD_products):
        self.repo = repo
    
    def insert_or_restock_product(self, product: ProductCreate):
        existing_product = self.repo.post_by_name(product)
        if existing_product:
            return self.repo.restock(existing_product, product)
        
        return self.repo.create_product(product)
    
    def search_products_by_optional_name_or_id(self, id: int = None, name: str = None):
        if name:
            name = name .capitalize()
        return self.repo.get_all_products(id, name)
    
    def search_one_product(self, product_id: int):
        return self.repo.get_by_id(product_id)
    
    def search_product_verific(self, id: int = None, name: str = None):
        return self.repo.search_by_name_and_id(id, name)
    
    def update_by_id(self, product_id: int, product_update: ProductCreate, name: str = None):
        product = self.repo.get_by_id_or_name(product_id, name)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Producto no encontrado.'
            )
        
        for field, value in product_update.model_dump().items():
                setattr(product, field, value)
        return self.repo.save_product(product)
    
    def update_stock_by_id(self, product_id: int, update_stock: int):
        self.repo.subtract_update_stock(product_id, update_stock)
    
    def add_update_stock(self, product_id: int, update_stock: int):
        product = self.repo.add_update_stock_product(product_id, update_stock)
        if not product:
            raise HTTPException(
                status_code=404,
                detail=f'No se ha encontrado el producto ID {product_id}.'
            )
        product.stock += update_stock
        if product.is_active == False:
            product.is_active = True
        self.repo.db.commit()
        self.repo.db.refresh(product)
        return product
    
    def soft_delete(self, product_id: int):
        product = self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Producto no encontrado.'
            )
        self.repo.soft_delete_modific(product)