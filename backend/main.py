from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, Form, UploadFile, File, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Any
import os
from backend.data_modules.database import get_db
from data_modules.models import User, Note
from sqlalchemy.orm import Session
import datetime
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DataError
from fastapi.responses import JSONResponse
from schemas import UserSchema, UserPublic, NoteSchema, Token, TokenData
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Diretório onde os arquivos serão salvos
UPLOAD_DIRECTORY = "uploads"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)  # Cria a pasta se não existir


app = FastAPI()

SECRET_KEY = "hello world"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 180


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Domínios permitidos
    allow_credentials=True,  # Permitir envio de cookies
    allow_methods=["*"],  # Métodos HTTP permitidos
    allow_headers=["*"],  # Cabeçalhos permitidos
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/register", status_code=201, response_model=UserPublic)
async def register( user: UserSchema,
    db:Session = Depends(get_db)
    ):

    hashed_password = get_password_hash(user.password)

    db_user = User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_user( username:str, db):
    user = db.query(User).filter(User.username == username).first()
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
    token: Annotated[str, Depends(oauth2_scheme)],
    db:Session = Depends(get_db)
    ):
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

# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)],
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user

@app.post("/login", status_code=200)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db:Session = Depends(get_db)
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

    return Token(access_token=access_token, token_type="bearer")




@app.post("/note", status_code=201, response_model=NoteSchema)
async def create_note( 
    current_user: Annotated[User, Depends(get_current_user)],
    note_title: str = Form(...),
    db:Session = Depends(get_db)
    ):

    db_note = Note(user_id=current_user.id, title=note_title, content="")
    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return db_note

@app.get("/note", response_model=list[NoteSchema])
async def get_all_notes(
    current_user: Annotated[User, Depends(get_current_user)],
    db:Session = Depends(get_db),
    ):
    notes = db.query(Note).filter(Note.user_id == current_user.id).all()

    
    return notes

@app.get("/note/{note_id}", response_model=NoteSchema)
async def get_note_by_id(
    current_user: Annotated[User, Depends(get_current_user)],
    note_id: int,
    db:Session = Depends(get_db)
    ):
    
    note = db.query(Note).filter(
        Note.id == note_id, 
        Note.user_id==current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.put("/note/{note_id}")
async def update_note(
    current_user: Annotated[User, Depends(get_current_user)],
    note_id: int,
    note_title: str = Form(...),
    note_content: str = Form(...),
    db:Session = Depends(get_db)):

    note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    
    if not note:
        # Lança exceção se não encontrar o registro
        raise HTTPException(status_code=404, detail="Note not found")
    
    note.title = note_title
    note.content = note_content
    note.updated_at = datetime.datetime.now(timezone.utc) 
    
    # Commit as mudanças no banco
    db.commit()
    db.refresh(note)
    return note


@app.delete("/note/{note_id}")
async def delete_note(
    current_user: Annotated[User, Depends(get_current_user)],
    note_id: int,
    db: Session = Depends(get_db)):
    # Busca a nota no banco de dados
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    
    if not note:
        # Lança exceção se não encontrar o registro
        raise HTTPException(status_code=404, detail="Note not found")
    
    # Remove a nota do banco de dados
    db.delete(note)
    db.commit()
    
    return {
        "message": "Note deleted successfully"
    }



@app.get("/protected-route")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}! This is a protected route."}