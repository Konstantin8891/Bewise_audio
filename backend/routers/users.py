from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

import sys
sys.path.append('..')

from database import SessionLocal
from schemas import UserSchema
from models import User


router = APIRouter(prefix='/users', tags=['users_router'])


def get_db() -> None:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.post('/create_user', status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserSchema, db: Session = Depends(get_db)
) -> List[Union[UUID, int]]:
    user_instance = db.query(User).filter(User.name == user.name).first()
    if user_instance:
        raise HTTPException(status_code=400, detail='User already exists')
    user_model = User(name=user.name)
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model.id, user_model.uuid
