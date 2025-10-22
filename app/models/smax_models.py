import json
from typing import Optional, Dict, Any
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeMeta
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.inspection import inspect
import requests
from app.config import settings
from app.logger import logger
from app.models.base import Base

#MODELS
from app.models.Control_model import Control
from app.models.TopDesk_model import TDIncident, TopDeskdata

DB_CONNECTION = settings.conn_str

def compare_ticket_model_and_db(pydantic_model: BaseModel, sqlalchemy_instance: DeclarativeMeta) -> Dict[str, Dict[str, Any]]:
    """
    Compare a Pydantic TicketModel instance with a SQLAlchemy Ticket instance.
    
    Returns a dict with keys as field names and values as a dict of 'db' and 'model' differing values.
    """
    differences = {}

    # Get all columns from the SQLAlchemy instance
    mapper = inspect(sqlalchemy_instance.__class__)
    if not mapper:
        logger.error("SQLAlchemy instance does not have a mapper.")
        return differences

    db_fields = {column.key for column in mapper.attrs}


    for field in pydantic_model.__class__.model_fields:
        if field in db_fields:
            model_value = getattr(pydantic_model, field, None)
            db_value = getattr(sqlalchemy_instance, field, None)

            # Normalize if needed
            if model_value != db_value:
                differences[field] = {
                    'db': db_value,
                    'model': model_value
                }

    return differences

class Ticket(Base):
    __tablename__ = 'tickets'

    ticket_id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    priority = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Ticket(ticket_id={self.ticket_id}, title={self.title}, status={self.status})>"
    


class TicketModel(BaseModel):

    ticket_id: str
    title: str
    priority: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = "open"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True