# File: tests/conftest.py
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.shared.infrastructure.persistence.database import Base, get_db
from src.user.domain.model.user import User
from src.shared.domain.value_objects import Email, Money
from fastapi.testclient import TestClient
from src.main import app
from decimal import Decimal
from src.order.domain.model.order import Order, OrderItem
from src.product.domain.model.product import Product
from src.auth.infrastructure.jwt_service import JWTService
from src.user.infrastructure.persistence.postgresql_user_repository import PostgresqlUserRepository

# Test database URL para SQLite en memoria
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    return engine

@pytest.fixture(scope="function")
def TestingSessionLocal(test_engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="function")
def test_session(test_engine, TestingSessionLocal):
    Base.metadata.create_all(bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
        Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope="function")
def test_db(test_engine, TestingSessionLocal):
    Base.metadata.drop_all(bind=test_engine)  # Limpiar primero
    Base.metadata.create_all(bind=test_engine)
    
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)
        if get_db in app.dependency_overrides:
            del app.dependency_overrides[get_db]

@pytest.fixture
def client(test_db):
    # No crear el usuario aquí, dejarlo para las pruebas específicas
    return TestClient(app)

@pytest.fixture
def sample_user_dict():
    return {
        "email": "test@example.com",
        "name": "Test User"
    }

@pytest.fixture
def sample_user(sample_user_dict):
    return User.create(
        email=sample_user_dict["email"],
        name=sample_user_dict["name"]
    )

@pytest.fixture
def mock_user():
    return User(
        id=1,
        email=Email(value="test@example.com"),
        name="Test User",
        created_at=datetime.utcnow()
    )

@pytest.fixture
def mock_user_service(mocker, mock_user):
    service = mocker.Mock()
    service.create_user.return_value = mock_user
    service.get_user_by_email.return_value = mock_user
    return service

@pytest.fixture
def mock_order_item():
    return OrderItem(
        id=1,
        product_name="Test Product",
        unit_price=Money(amount=Decimal("10.00")),
        quantity=2
    )

@pytest.fixture
def mock_order(mock_user, mock_order_item):
    return Order(
        id=1,
        customer_name="Test Customer",
        items=[mock_order_item],
        waiter_id=mock_user.id,
        created_at=datetime.utcnow()
    )

@pytest.fixture
def mock_product():
    now = datetime.utcnow()
    return Product(
        id=1,
        name="Test Product",
        current_price=Money(amount=Decimal("10.00")),
        created_at=now,
        updated_at=now
    )

@pytest.fixture
def mock_product_service(mocker, mock_product):
    service = mocker.Mock()
    service.get_all_products.return_value = [mock_product]
    service.get_product_by_name.return_value = mock_product
    service.create_or_update_product.return_value = mock_product
    return service

@pytest.fixture
def test_user(test_db):
    """Crea un usuario de prueba en la base de datos"""
    repository = PostgresqlUserRepository(test_db)
    user = User.create(
        email="test@example.com",
        name="Test User"
    )
    created_user = repository.save(user)
    test_db.commit()
    return created_user

@pytest.fixture
def auth_token(test_user):
    """Crea un token JWT válido para el usuario de prueba"""
    return JWTService.create_access_token({
        "sub": str(test_user.email),
        "user_id": test_user.id
    })

@pytest.fixture
def auth_headers(auth_token):
    """Headers de autenticación con un token JWT válido"""
    return {"Authorization": f"Bearer {auth_token}"}

@pytest.fixture
def mock_auth_headers():
    """Headers con un token mock para pruebas que no requieren validación real"""
    return {"Authorization": "Bearer test-token"}
