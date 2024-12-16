from fastapi import FastAPI, Form, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any
import os
from data_modules.config import SessionLocal, engine
from data_modules.models import User, Note, Teste1
from sqlalchemy.orm import Session
import datetime
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DataError
from fastapi.responses import JSONResponse
from schemas import UserSchema, UserPublic, NoteSchema


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

@app.post("/register", status_code=201, response_model=UserPublic)
async def register( user: UserSchema,
    db:Session = Depends(get_db)
    ):

    db_user = User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@app.post("/login")
async def login( username: str = Form(...), password: str = Form(...)):
    
    
    return {
        "message": "login",
    }



@app.post("/note", status_code=201, response_model=NoteSchema)
async def create_note( 
    note_title: str = Form(...), 
    db:Session = Depends(get_db) ):

    db_note = Note( title=note_title, content="" )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@app.get("/note", response_model=list[NoteSchema])
async def get_all_notes(
    db:Session = Depends(get_db)
    ):

    notes = db.query(Note).all()
    return notes

@app.get("/note/{note_id}", response_model=NoteSchema)
async def get_note_by_id(
    note_id: int,
    db:Session = Depends(get_db)
    ):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.put("/note/{note_id}")
async def update_note(
    note_id: int,
    note_content: str = Form(...),
    db:Session = Depends(get_db)):

    note = db.query(Note).filter(Note.id == note_id).first()
    
    if not note:
        # Lança exceção se não encontrar o registro
        raise HTTPException(status_code=404, detail="Note not found")
    
    note.content = note_content
    note.updated_at = datetime.datetime.now(datetime.timezone.utc) 
    
    # Commit as mudanças no banco
    db.commit()
    db.refresh(note)
    return note


@app.delete("/note/{note_id}")
async def delete_note(note_id: int, db: Session = Depends(get_db)):
    # Busca a nota no banco de dados
    note = db.query(Note).filter(Note.id == note_id).first()
    
    if not note:
        # Lança exceção se não encontrar o registro
        raise HTTPException(status_code=404, detail="Note not found")
    
    # Remove a nota do banco de dados
    db.delete(note)
    db.commit()
    
    return {
        "message": "Note deleted successfully"
    }