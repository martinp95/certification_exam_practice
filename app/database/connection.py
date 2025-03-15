import os
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Load environment variables with defaults
POSTGRES_USER = os.getenv("POSTGRES_USER", "certification_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "certification_password")
POSTGRES_DB = os.getenv("POSTGRES_DB", "certification_db")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# Encode password to handle special characters
encoded_password = urllib.parse.quote_plus(POSTGRES_PASSWORD)

# Allow DATABASE_URL override (for cloud deployments)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql://{POSTGRES_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"
)

# Create database engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=10,         # Maintain up to 10 connections in the pool
    max_overflow=20,      # Allow up to 20 additional connections
    pool_pre_ping=True,   # Check connections before using them
    connect_args={"options": "-c timezone=utc"}  # Set UTC timezone
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()


def get_db():
    """
    Dependency to provide a database session.

    Yields:
        Session: A SQLAlchemy session.

    Raises:
        HTTPException: If there is an issue connecting to the database.
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()  # Rollback transaction in case of error
        raise e
    finally:
        db.close()
