from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.sale import SaleCreate, SaleResponde
from app.schemas.sale import SaleUpdateStatus
from app.schemas.sale_details import SaleDetailsResponse
from app.api.depends.deps_sale.sale import get_sale_service
from app.services.sale_service import SaleService

router = APIRouter(prefix='/sale', tags=['Sale'])

@router.post('/sale', response_model=SaleResponde, status_code=status.HTTP_201_CREATED)
def add_product_sale(sale_data: SaleCreate, serviceSale: SaleService = Depends(get_sale_service)):
    return serviceSale.verific_and_add_product_sale(sale_data)

@router.patch('/sale/{sale_id}', response_model=list[SaleDetailsResponse], status_code=status.HTTP_200_OK)
def pay(sale_id: int, status_sale: SaleUpdateStatus, serviceSale: SaleService = Depends(get_sale_service)):
    return serviceSale.pay_or_cancel(sale_id, status_sale)