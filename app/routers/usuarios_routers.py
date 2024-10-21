from typing import List
from fastapi import APIRouter, HTTPException
from app.models.usuarios_models import Usuario

router = APIRouter()

usuarios = []
contador_usuario = 1

@router.post("/usuarios/", response_model=Usuario)
def criar_usuario(nome: str):
    global contador_usuario
    novo_usuario = Usuario(id=contador_usuario, nome=nome)
    usuarios.append(novo_usuario)
    contador_usuario += 1
    return novo_usuario

@router.get("/usuarios/", response_model=List[Usuario])
def listar_usuarios():
    return usuarios