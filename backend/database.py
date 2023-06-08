from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext import asyncio as sea
from sqlalchemy.ext.declarative import declarative_base

from settings import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, HOST


load_dotenv()

SQLALCHEMY_DATABASE_URL = (
    f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{HOST}/'
    f'{POSTGRES_DB}'
)

engine = sea.create_async_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=sea.AsyncSession,
)


async def get_async_session() -> AsyncGenerator[sea.AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


Base = declarative_base()
