from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .deps import redis_cache, get_async_session
from .database.schemas import User, UserOut

router = APIRouter()


@router.get("/")
async def handle_read_root():
    return await redis_cache.read_root()


@router.post("/users")
async def create_user(
    user: User, db_session: AsyncSession = Depends(get_async_session)
) -> UserOut:
    return await redis_cache.create_user(user, db_session)


@router.get("/users")
async def read_users(
    db_session: AsyncSession = Depends(get_async_session)
) -> list[UserOut]:
    return await redis_cache.read_users(db_session)


@router.get("/users/{user_id}")
async def read_user(
    user_id: int,
    db_session: AsyncSession = Depends(get_async_session)
) -> UserOut:
    return await redis_cache.read_user(user_id, db_session)


@router.put("/users/{user_id}")
async def update_user(
    user_id: int,
    user: User,
    db_session: AsyncSession = Depends(get_async_session)
) -> UserOut:
    return await redis_cache.update_user(user_id, user, db_session)


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db_session: AsyncSession = Depends(get_async_session)
) -> dict:
    return await redis_cache.delete_user(user_id, db_session)


@router.post("/login")
async def login(
    user: User, db_session: AsyncSession = Depends(get_async_session)
) -> dict:
    return await redis_cache.login(user, db_session)
