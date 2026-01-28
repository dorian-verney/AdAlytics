from sqlalchemy.ext.asyncio import (create_async_engine, 
                                    async_sessionmaker, 
                                    AsyncSession)
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os
from sqlalchemy import Column, Integer, String
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)
session_factory = async_sessionmaker(autocommit=False, 
                                                autoflush=False, 
                                                bind=engine)
class Base(DeclarativeBase):
    pass


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session():
    async with session_factory() as session:
        yield session

