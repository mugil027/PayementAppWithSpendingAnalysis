# File: Backend/app/database.py
# Description: Database connection and session management.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings # Import the settings object

# The engine is the main entry point to the database.
# It now uses the DATABASE_URL from our settings.
# The 'connect_args' are only needed for SQLite.
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Each instance of SessionLocal will be a database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This Base class will be inherited by all our database models (the ORM models).
Base = declarative_base()

# --- Dependency for API routes ---
def get_db():
    """
    A dependency that provides a database session to API routes
    and ensures it's closed after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
