from backend.data_modules.database import get_session
from backend.data_modules.models import User, Note
from sqlalchemy.orm import Session
import datetime
from backend.schemas import NoteSchema, MessageSchema
from typing import Annotated
from fastapi import APIRouter, Form, Depends, HTTPException
from backend.security import get_current_user
from datetime import timezone

router = APIRouter(prefix='/note', tags=['notes'])
DbSession = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

@router.post("/", status_code=201, response_model=NoteSchema)
async def create_note( 
    current_user: CurrentUser,
    db:DbSession,
    note_title: str = Form(...)
    ):

    db_note = Note(user_id=current_user.id, title=note_title, content="")
    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return db_note

@router.get("/", response_model=list[NoteSchema])
async def get_all_notes(
    current_user: CurrentUser,
    db:DbSession,
    ):
    notes = db.query(Note).filter(Note.user_id == current_user.id).all()

    
    return notes

@router.get("/{note_id}", response_model=NoteSchema)
async def get_note_by_id(
    current_user: CurrentUser,
    note_id: int,
    db:DbSession
    ):
    
    note = db.query(Note).filter(
        Note.id == note_id, 
        Note.user_id==current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.put("/{note_id}", response_model=NoteSchema)
async def update_note(
    current_user: CurrentUser,
    note_id: int,
    db:DbSession,
    note_title: str = Form(...),
    note_content: str = Form(...)):

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


@router.delete("/{note_id}", response_model=MessageSchema)
async def delete_note(
    current_user: CurrentUser,
    note_id: int,
    db: DbSession):
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
