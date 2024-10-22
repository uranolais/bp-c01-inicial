from fastapi import FastAPI
from app.routers import produtos_routers,usuarios_routers
from typing import Dict

app = FastAPI()

app.include_router(produtos_routers.router)
app.include_router(usuarios_routers.router)

MENSAGEM_HOME: str    ="Bem-vindo à API de Recomendação de Produtos"

# Iniciando o servidor
@app.get("/", response_model = Dict[str,str])
def home() -> Dict[str,str]:
    global MENSAGEM_HOME
    return {"mensagem": MENSAGEM_HOME}
