import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app
from models.user import User
from models.service import Service
from schemas.user import UserCreate
from crud.crud_user import CRUDUser
from datetime import datetime, timedelta

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def test_user_data():
    return {"email": "test@example.com", "password": "password"}

@pytest.fixture(scope="module")
def test_admin_data():
    return {"email": "admin@example.com", "password": "password", "is_admin": True}


@pytest.fixture(scope="module")
def test_user(client, test_user_data):
    response = client.post("/users/", json=test_user_data)
    assert response.status_code == 200
    return response.json()

@pytest.fixture(scope="module")
def test_admin(client, test_admin_data):
    response = client.post("/users/", json=test_admin_data)
    assert response.status_code == 200
    return response.json()


@pytest.fixture(scope="module")
def test_service(client, test_user):
    headers = {"Authorization": f'''Bearer {client.post("/auth/token", data={"username": test_user["email"], "password": "password"}).json()["access_token"]}'''}
    service_data = {"name": "Test Service", "description": "A service for testing", "price": 100.0}
    response = client.post("/services/", json=service_data, headers=headers)
    assert response.status_code == 200
    return response.json()