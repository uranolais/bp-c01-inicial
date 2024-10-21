from fastapi import FastAPI
from app.routers import *

app = FastAPI()

app.include_router(router)

MENSAGEM_HOME    ="Bem-vindo à API de Recomendação de Produtos"

# Iniciando o servidor
@app.get("/")
def home():
    global MENSAGEM_HOME
    return {"mensagem": MENSAGEM_HOME}
