from app.schemas.product import ProductCreate

from fastapi import HTTPException, status
from app.repositories.product_repository import CRUD_products

class ProductServices:
    def __init__(self, repo: CRUD_products):
        self.repo = repo
    
    def add(self, product: ProductCreate):
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
    
    def soft_delete(self, product_id: int):
        product = self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Producto no encontrado.'
            )
        self.repo.soft_delete_modific(product)