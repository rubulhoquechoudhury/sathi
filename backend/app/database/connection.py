"""
Database Connection Manager supporting MySQL 8+ via PyMySQL
with automatic local SQLite fallback for offline testing.
"""

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    """SQLAlchemy Declarative Base Model."""
    pass


def create_db_engine():
    """Create SQLAlchemy engine with MySQL -> SQLite fallback."""
    db_url = settings.DATABASE_URL
    try:
        if db_url.startswith("mysql"):
            # Test MySQL connection parameters
            engine = create_engine(
                db_url,
                pool_size=10,
                max_overflow=20,
                pool_recycle=3600,
                connect_args={"connect_timeout": 5}
            )
            # Verify connection with a quick ping
            with engine.connect() as conn:
                pass
            logger.info("Successfully connected to MySQL database.")
            return engine
    except Exception as err:
        logger.warning(f"Could not connect to MySQL database at {db_url}: {err}. Falling back to local SQLite database: sqlite:///./landslide_system.db")

    # Fallback to local SQLite database for offline development & testing
    fallback_url = "sqlite:///./landslide_system.db"
    return create_engine(fallback_url, connect_args={"check_same_thread": False})


engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database tables and seed initial data if empty."""
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables initialized successfully.")
    try:
        from app.database.seed import seed_initial_data
        db = SessionLocal()
        try:
            seed_initial_data(db)
        finally:
            db.close()
    except Exception as err:
        logger.warning(f"Seed initialization warning: {err}")



def get_db():
    """FastAPI Session Dependency Injector."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
