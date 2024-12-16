from pydantic import BaseModel
from datetime import datetime
class UserSchema(BaseModel):
    username: str
    password: str

class UserPublic(BaseModel):
    id: int
    username: str

class NoteSchema(BaseModel):
    id: int
    title:str
    content:str
    created_at:datetime
    updated_at:datetime

