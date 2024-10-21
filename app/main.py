from fastapi import FastAPI
from app.routers import produtos_routers,usuarios_routers

app = FastAPI()

app.include_router(produtos_routers.router)
app.include_router(usuarios_routers.router)

MENSAGEM_HOME    ="Bem-vindo à API de Recomendação de Produtos"

# Iniciando o servidor
@app.get("/")
def home():
    global MENSAGEM_HOME
    return {"mensagem": MENSAGEM_HOME}
