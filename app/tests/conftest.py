import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from models.base import Base
from app.core.db_helper import db_helper

# Use the synchronous postgres driver
DATABASE_URL = "postgresql://bekzod:admin123@localhost:5436/test_db"

# Setup Sync Engine
engine = create_engine(DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create tables once for the entire test session."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    """Provides a transactional session that rolls back after each test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    """Provides a test client with overridden database dependency."""
    def override_get_db():
        yield db_session
    
    app.dependency_overrides[db_helper.session_getter] = override_get_db
    
    with TestClient(app) as c:
        yield c
    
    app.dependency_overrides.clear()


