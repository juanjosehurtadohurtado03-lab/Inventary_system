from fastapi import Depends
from sqlalchemy.orm import Session
from app.repositories.sale_repository import CRUD_sale
from app.database.connect import get_db

def get_crud_sale(db: Session = Depends(get_db)) -> CRUD_sale:
    return CRUD_sale(db)