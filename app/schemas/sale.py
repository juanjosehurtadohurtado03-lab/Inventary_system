from pydantic import BaseModel, Field

class SaleCreate(BaseModel):
    date: str
    time: str
    total: int = Field(ge=1, description='El valor no puede ser negativo.')

class SaleResponse(BaseModel):
    date: str
    time: str
    total: int
    status: str