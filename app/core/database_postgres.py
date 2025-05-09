import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from dotenv import load_dotenv
from app.utils.logger import get_logger

# Load environment variables
load_dotenv()

# Initialize logger
logger = get_logger(__name__)

# Get database URL securely
DATABASE_URL = os.getenv("DATABASE_POSTGRES_URL")
logger.info(f"Postgre db url loaded")


if not DATABASE_URL:
    logger.critical("DATABASE_URL is not set in the environment variables!")
    raise ValueError("DATABASE_URL is missing")

logger.info("Database URL successfully loaded")
# Create engine
engine = None

def verify_postgres_connection():
    global engine
    try:
        engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        logger.info("Connected to PostgreSQL successfully")
    except Exception as e:
        logger.error(f"Failed to create database engine: {e}")
        raise

# Session factory
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base class for models
Base = declarative_base()

# Dependency for DB sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from app.modules.user.models.user import User

    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully.")
