from pydantic import BaseModel
from typing import List
from fastapi import APIRouter, HTTPException
from fastapi import FastAPI

# Modelo base para produto
class ProdutoBase(BaseModel):
    nome: str
    categoria: str
    tags: List[str]

# Modelo para criar um produto
class CriarProduto(ProdutoBase):
    pass

# Modelo de produto com ID
class Produto(ProdutoBase):
    id: int

# Modelo para histórico de compras do usuário
class HistoricoCompras(BaseModel):
    produtos_ids: List[int]

# Modelo para preferências do usuário
class Preferencias(BaseModel):
    categorias: List[str] | None = None
    tags: List[str] | None = None

# roteador = APIRouter()

# Armazenamento em memória
produtos         =[]
contador_produto =1
MENSAGEM_HOME    ="Bem-vindo à API de Recomendação de Produtos"

# Histórico de compras em memória
historico_compras = {}
app = FastAPI()

# Iniciando o servidor
@app.get("/")
def home():
    global MENSAGEM_HOME
    return {"mensagem": MENSAGEM_HOME}

# Rota para cadastrar produtos
@app.post("/produtos/", response_model=Produto)
def criar_produto(produto: CriarProduto):
    global contador_produto
    novo_produto = Produto(id=contador_produto, **produto.dict())
    produtos.append(novo_produto)
    contador_produto += 1
    return novo_produto

# Rota para listar todos os produtos
@app.get("/produtos/", response_model=List[Produto])
def listar_produtos():
    return produtos

# Rota para simular o histórico de compras de um usuário
@app.post("/historico_compras/{usuario_id}")
def adicionar_historico_compras(usuario_id: int, compras: HistoricoCompras):
    historico_compras[usuario_id] = compras.produtos_ids
    return {"mensagem": "Histórico de compras atualizado"}

# Rota para recomendações de produtos
@app.post("/recomendacoes/{usuario_id}", response_model=List[Produto])
def recomendar_produtos(usuario_id: int, preferencias: Preferencias):
    if usuario_id not in historico_compras:
        print("Histórico de compras não encontrado")
        # raise HTTPException(status_code=404, detail="Histórico de compras não encontrado")

    produtos_recomendados = []

    # Buscar produtos com base no histórico de compras do usuário
    for produto_id in historico_compras[usuario_id]:
        for produto in produtos:
            if produto.id == produto_id:
                produtos_recomendados.append(produto)

    # produtos_recomendados = [produto for produto_id in historico_compras[usuario_id] for produto in produtos if produto.id == produto_id]
    '''
    produtos_recomendados = [
        produto
        for produto_id in historico_compras[usuario_id]
        for produto in produtos
        if produto.id == produto_id
    ]
    '''

    # Filtrar as recomendações com base nas preferências
    if preferencias.categorias:
        produtos_filtrados = []
        for p in produtos_recomendados:
            if p.categoria in preferencias.categorias:
                produtos_filtrados.append(p)
        produtos_recomendados = produtos_filtrados
        # produtos_recomendados = [p for p in produtos_recomendados if p.categoria in preferencias.categorias]
        # produtos_recomendados = [
        #     p
        #     for p in produtos_recomendados
        #     if p.categoria in preferencias.categorias
        # ]

    if preferencias.tags:
        produtos_filtrados = []
        for p in produtos_recomendados:
            if any(tag in preferencias.tags for tag in p.tags):
                produtos_filtrados.append(p)
        produtos_recomendados = produtos_filtrados
        # produtos_recomendados = [p for p in produtos_recomendados if any(tag in preferencias.tags for tag in p.tags)]

    return produtos_recomendados
