from pydantic import BaseModel, ConfigDict

class SaleDetailsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    quantity: int
    price_unit: int
    subtotal: int