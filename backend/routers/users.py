from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.data_modules.database import get_session
from backend.data_modules.models import User

from backend.schemas import UserPublic, UserSchema
from auth import get_current_user, get_password_hash


router = APIRouter(prefix='/users', tags=['users'])
DbSession = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

@router.post("/register", status_code=201, response_model=UserPublic)
async def register( user: UserSchema,
    db:DbSession
    ):

    hashed_password = get_password_hash(user.password)

    db_user = User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
