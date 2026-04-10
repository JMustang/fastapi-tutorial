from collections.abc import AsyncGenerator
import uuid
import os
from dotenv import load_dotenv

from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship

load_dotenv()
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://fastapi_user:fastapi_password@localhost:5432/fastapi_db",
)
