import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from fastapi.testclient import TestClient
from app.database.connect import get_db
from app.database.base import Base
from app.core.config import TEST_DATABASE_URL
from app.models.product import ProductModel
from app.models.sale import SaleModel
from app.models.sale_details import SaleDetailsModel

engine = create_engine(TEST_DATABASE_URL, connect_args={'check_same_thread': False}, poolclass=StaticPool)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope='function')
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)