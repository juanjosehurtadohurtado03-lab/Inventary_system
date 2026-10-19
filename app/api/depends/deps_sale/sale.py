from fastapi import Depends
from app.api.depends.deps_sale.db_sale import get_crud_sale
from app.services.sale_service import SaleService
from app.repositories.sale_repository import CRUD_sale
from app.services.products_service import ProductServices
from app.api.depends.deps_product.product import get_product_service

def get_sale_service(db_sale: CRUD_sale = Depends(get_crud_sale), db_product: ProductServices = Depends(get_product_service)) -> SaleService:
    return SaleService(db_sale, db_product)