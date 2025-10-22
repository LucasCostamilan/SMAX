from sqlalchemy import create_engine
from app.config import settings
from app.models.base import Base
from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects import mysql

#logging
from app.logger import logger

#Model
from app.models.Control_model import Control
from app.models.smax_models import Ticket

DB_CONNECTION = settings.conn_str

def init_db():
    """
    Initialize the database and create tables if they do not exist.
    """
    try:
        # Create an engine
        engine = create_engine(DB_CONNECTION, echo=True, future=True)

        # Create all tables in the database
        Base.metadata.create_all(engine)

        # Log the successful initialization
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
