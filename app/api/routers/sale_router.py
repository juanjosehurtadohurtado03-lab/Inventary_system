from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.sale import SaleCreate, SaleResponde
from app.models.sale import SaleModel
from app.api.depends.deps_sale.sale import get_sale_service
from app.services.sale_service import SaleService

router = APIRouter(prefix='/sale', tags=['Sale'])

@router.post('/', response_model=SaleResponde, status_code=status.HTTP_201_CREATED)
def add_product_sale(sale_data: SaleCreate, serviceSale: SaleService = Depends(get_sale_service)):
    return serviceSale.verific_and_add_product_sale(sale_data)

