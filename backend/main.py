from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any
import os

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


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/data")
async def post_one( user: str = Form(...),
    password: str = Form(...),
    photo: UploadFile = File(...)
    ):


    
     # Define o caminho completo para salvar o arquivo
    file_path = os.path.join(UPLOAD_DIRECTORY, photo.filename)

    # Lê e grava o arquivo no diretório
    with open(file_path, "wb") as file:
        file_content = await photo.read()  # Lê o conteúdo do arquivo
        file.write(file_content)  # Salva no disco


    print("User:", user)
    print("Password:", password)
    print("Photo filename:", photo.filename)
    print("File size (bytes):", len(file_content))
    return {
        "message": "Dados recebidos com sucesso!",
        "user": user,
        "photo_filename": photo.filename
    }