from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from backend.data_modules.database import get_session
from backend.data_modules.models import User
from jwt.exceptions import InvalidTokenError
from schemas import TokenData


SECRET_KEY = "hello world"
ALGORITHM = "HS256"
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
router = APIRouter(prefix='/auth', tags=['auth'])

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
DbSession = Annotated[Session, Depends(get_session)]


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(username:str, db):
    user = db.scalar(select(User).where(User.username == username))
    return user

def authenticate_user(username: str, password: str, db):
    user = get_user(username, db)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    token: OAuth2Form,
    db:DbSession):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(username=token_data.username, db=db)
    if user is None:
        raise credentials_exception
    return user