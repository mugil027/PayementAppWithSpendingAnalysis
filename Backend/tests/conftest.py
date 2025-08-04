# File: Backend/tests/conftest.py
# Description: Configuration for the pytest test suite.

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# --- Test Database Setup ---
# Use an in-memory SQLite database for fast, isolated tests.
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables before tests run, drop them after.
Base.metadata.create_all(bind=engine)

# --- Test Dependency Override ---
def override_get_db():
    """
    A dependency that provides a test database session.
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Apply the override to the main app.
app.dependency_overrides[get_db] = override_get_db

# --- Pytest Fixture for the API Client ---
@pytest.fixture(scope="module")
def client():
    """
    Provides a TestClient instance for making API requests in tests.
    """
    with TestClient(app) as c:
        yield c
    # Clean up the database file after tests are done
    import os
    os.remove("./test.db")

