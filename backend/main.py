from fastapi import FastAPI, Form, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any
import os
from data_modules.config import SessionLocal, engine
from data_modules.models import User, Note
from sqlalchemy.orm import Session
import datetime

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

@app.post("/login")
async def login( user: str = Form(...), password: str = Form(...)):
    return {
        "message": "login",
    }



@app.post("/note")
async def create_note( 
    note_title: str = Form(...), 
    db:Session = Depends(get_db) ):
    db_note = Note( title=note_title, content="" )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return {
        "message": "login",
    }

@app.get("/note")
async def get_all_notes(
    db:Session = Depends(get_db)
    ):

    notes = db.query(Note).all()
    return notes

@app.get("/note/{note_id}")
async def get_note_by_id(
    note_id: int,
    db:Session = Depends(get_db)
    ):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.put("/note/{note_id}")
async def update_task(
    note_id: int,
    note_content: str = Form(...),
    db:Session = Depends(get_db)):

    note = db.query(Note).filter(Note.id == note_id).first()
    
    if not note:
        # Lança exceção se não encontrar o registro
        raise HTTPException(status_code=404, detail="Note not found")
    
    note.content = note_content
    note.updated_at = datetime.datetime.now(datetime.timezone.utc)  # Atualiza a data de modificação
    
    # Commit as mudanças no banco
    db.commit()
    db.refresh(note)
    return {
        "message": "login",
    }