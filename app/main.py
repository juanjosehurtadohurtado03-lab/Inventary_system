from fastapi import FastAPI
from app.api.routers.products_router import router as products_router

from app.database.base import Base
from app.database.connect import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Sistema de Inventario y Facturacion',
    version='1.0.0',
    description='API RESTful de inventario y ventas.'
)

app.include_router(products_router ,prefix='/api/routers')