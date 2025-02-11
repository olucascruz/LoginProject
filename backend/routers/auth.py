from datetime import timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.data_modules.database import get_session
from backend.schemas import TokenSchema
from backend.security import create_access_token, authenticate_user, get_current_user
from backend.data_modules.models import User

SECRET_KEY = "hello world"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 180
router = APIRouter(prefix='/auth', tags=['auth'])
CurrentUser = Annotated[User, Depends(get_current_user)]

DbSession = Annotated[Session, Depends(get_session)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post("/login", status_code=200, response_model=TokenSchema)
async def login(
    form_data: OAuth2Form,
    db:DbSession
    ):
    
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"})
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return TokenSchema(access_token=access_token, token_type="bearer")


@router.post('/refresh_token', response_model=TokenSchema)
def refresh_access_token(
    user: CurrentUser,
):
    new_access_token = create_access_token(data={'sub': user.username})

    return {'access_token': new_access_token, 'token_type': 'bearer'}