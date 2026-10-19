from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.product import ProductCreate, ProductResponse
from app.services.products_service import ProductServices
from app.api.depends.deps_product.product import get_product_service

router = APIRouter(prefix='/product', tags=['Products'])

@router.post('/', response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def add_product(product: ProductCreate, serviceProduct: ProductServices = Depends(get_product_service)):
    return serviceProduct.add(product)

@router.get('/', response_model=list[ProductResponse])
def search_products(id: int = None, name: str = None, serviceProduct: ProductServices = Depends(get_product_service)):
    return serviceProduct.search_products_by_optional_name_or_id(id, name)

@router.put('/{product_id}', response_model=ProductResponse)
def update_product(product_id: int, product_update: ProductCreate, name: str = None, serviceProduct: ProductServices = Depends(get_product_service)):
    return serviceProduct.update_by_id(product_id, product_update, name)

@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
def soft_delete_product(product_id: int, serviceProduct: ProductServices = Depends(get_product_service)):
    return serviceProduct.soft_delete(product_id)