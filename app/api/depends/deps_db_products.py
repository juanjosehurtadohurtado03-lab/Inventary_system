from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.connect import get_db
from app.repositories.product_repository import CRUD_products

def get_crud_product(db: Session = Depends(get_db)) -> CRUD_products:
    return CRUD_products(db)