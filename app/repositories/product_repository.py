from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.product import ProductModel
from app.schemas.product import ProductCreate

class CRUD_products:
    def __init__(self, db: Session):
        self.db = db
        
    def post_by_name(self, product: ProductCreate):
        return self.db.query(ProductModel).filter(ProductModel.name.ilike(f'%{product.name}%')).first()

    def get_all_products(self, id: int = None, name: str = None):
        if id or name:
            if id and name:
                return self.db.query(ProductModel).filter(ProductModel.id == id, ProductModel.name == name, ProductModel.is_active == True).all()
            elif id:
                return self.db.query(ProductModel).filter(ProductModel.id == id, ProductModel.is_active == True).all()
            elif name:
                return self.db.query(ProductModel).filter(ProductModel.name.ilike(f'%{name}%'), ProductModel.is_active == True).all()
        return self.db.query(ProductModel).filter(ProductModel.is_active == True).all()
    
    def search_by_name_and_id(self, id: int = None, name: str = None):
        if id or name:
            if id and name:
                return self.db.query(ProductModel).filter(ProductModel.id == id, ProductModel.name == name, ProductModel.is_active == True).first()
            elif id:
                return self.db.query(ProductModel).filter(ProductModel.id == id, ProductModel.is_active == True).first()
            elif name:
                return self.db.query(ProductModel).filter(ProductModel.name.ilike(f'%{name}%'), ProductModel.is_active == True).first()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Campos en blanco no disponibles.'
            )

    def get_by_id(self, product_id: int):
        return self.db.query(ProductModel).filter(ProductModel.id == product_id, ProductModel.is_active == True).first()

    def get_by_id_or_name(self, product_id: int, name: str):
        return self.db.query(ProductModel).filter((ProductModel.id == product_id) | (ProductModel.name.ilike(f'%{name}%')), ProductModel.is_active == True).first()

    def restock(self, product: ProductModel, product_change: ProductCreate):
        if product_change.price:
            product.stock += product_change.stock
            product.price = product_change.price
        else:
            product.stock += product_change.stock
        product.is_active = True
        self.db.commit()
        self.db.refresh(product)
        return product

    def create_product(self, product: ProductCreate):
        new_product = ProductModel(**product.model_dump())
        self.db.add(new_product)
        self.db.commit()
        self.db.refresh(new_product)
        return new_product
    
    def save_product(self, product: ProductModel):
        self.db.commit()
        self.db.refresh(product)
        return product
    
    def update_stock(self, product_id: int, update_stock: int):
        product = self.db.query(ProductModel).filter(ProductModel.id == product_id, ProductModel.is_active == True).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Lo siento, ha ocurrido un error desconodico.'
            )
        product.stock = update_stock
        if product.stock == 0:
            product.is_active = False
        self.db.commit()
        self.db.refresh(product)
    
    def soft_delete_modific(self, product: ProductModel):
        product.is_active = False
        self.db.commit()