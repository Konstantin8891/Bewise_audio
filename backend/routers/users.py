from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext import asyncio as sea
from uuid import UUID

from database import get_async_session
from schemas import UserSchema
from models import User


router = APIRouter(prefix='/users', tags=['users_router'])


@router.post('/create_user', status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserSchema, db: sea.AsyncSession = Depends(get_async_session)
) -> List[Union[UUID, int]]:
    user_instance = await db.execute(select(User).where(
        User.name == user.name
    ))
    user_instance = user_instance.scalar_one_or_none()
    if user_instance:
        raise HTTPException(status_code=400, detail='User already exists')
    user_model = User(name=user.name)
    db.add(user_model)
    await db.commit()
    await db.refresh(user_model)
    return user_model.id, user_model.uuid
