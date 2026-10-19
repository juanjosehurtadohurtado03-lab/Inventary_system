from fastapi import Depends
from app.repositories.product_repository import CRUD_products
from app.api.depends.deps_product.db_products import get_crud_product
from app.services.products_service import ProductServices

def get_product_service(db: CRUD_products = Depends(get_crud_product)) -> ProductServices:
    return ProductServices(db)