"""PostgreSQL configuration module."""

import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column

POSTGRES_DB = os.getenv("POSTGRES_DB", "fever_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "fever_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "fever_pass")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", str(5432))

SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)


DB = SQLAlchemy(model_class=Base)
