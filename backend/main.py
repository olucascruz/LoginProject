from fastapi import FastAPI, Form, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any
import os
from data_modules.config import SessionLocal, engine
from data_modules.models import User
from sqlalchemy.orm import Session

# Diretório onde os arquivos serão salvos
UPLOAD_DIRECTORY = "uploads"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)  # Cria a pasta se não existir


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Domínios permitidos
    allow_credentials=True,  # Permitir envio de cookies
    allow_methods=["*"],  # Métodos HTTP permitidos
    allow_headers=["*"],  # Cabeçalhos permitidos
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/data")
async def post_one( user: str = Form(...),
    password: str = Form(...),
    photo: UploadFile = File(...),
    db:Session = Depends(get_db)
    ):

    db_user = User(username=user, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    
    print("User:", user)
    print("Password:", password)
    print("Photo filename:", photo.filename)
    return {
        "message": "Dados recebidos com sucesso!",
        "user": user,
        "photo_filename": photo.filename
    }