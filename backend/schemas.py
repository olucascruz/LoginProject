from pydantic import BaseModel
from datetime import datetime

class MessageSchema(BaseModel):
    message: str

class UserSchema(BaseModel):
    username: str
    password: str

class UserPublic(BaseModel):
    id: int
    username: str

class NoteSchema(BaseModel):
    id: int
    user_id: int
    title:str
    content:str
    created_at:datetime
    updated_at:datetime


class TokenSchema(BaseModel):
    access_token: str
    token_type: str

class TokenDataSchema(BaseModel):
    username: str | None = None