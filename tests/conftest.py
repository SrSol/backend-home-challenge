# File: tests/conftest.py
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.shared.infrastructure.persistence.database import Base, get_db
from src.user.domain.model.user import User
from src.shared.domain.value_objects import Email
from fastapi.testclient import TestClient
from src.main import app

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
        session.close()
        Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope="function")
def test_db(test_engine, TestingSessionLocal):
    Base.metadata.create_all(bind=test_engine)
    
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestingSessionLocal()
    
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def client(test_db):
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
