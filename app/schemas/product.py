from pydantic import BaseModel, Field, field_validator

class ProductCreate(BaseModel):
    name: str
    price: int = Field(ge=1, description='El precio no puede ser negativo.')
    stock: int = Field(ge=1, description='El precio no puede ser negativo.')
    
    @field_validator('name', mode='before')
    @classmethod
    def clean_name(cls, value: str):
        if isinstance(value, str):
            return value.strip().title()
        return value

class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    stock: int