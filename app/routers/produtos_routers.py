from typing import List, Dict
from fastapi import APIRouter, HTTPException
from app.models.produtos_models import (
    Produto,
    CriarProduto,
    HistoricoCompras,
    Preferencias,
)
from .usuarios_routers import usuarios

router = APIRouter()

# Armazenamento em memória
produtos: List[Produto] = []
contador_produto: int = 1

# Histórico de compras em memória
historico_compras: Dict[int, List[int]] = {}


@router.post("/produtos/", response_model=Produto)
def criar_produto(produto: CriarProduto) -> Produto:
    """
    Cria um novo produto.

    Args:
        produto (CriarProduto): O objeto contendo os dados do produto a ser criado.

    Returns:
        Produto: O objeto do produto recém-criado com um ID gerado.
    """
    global contador_produto
    novo_produto = Produto(id=contador_produto, **produto.model_dump())
    produtos.append(novo_produto)
    contador_produto += 1
    return novo_produto


@router.get("/produtos/", response_model=List[Produto])
def listar_produtos() -> List[Produto]:
    """
    Lista todos os produtos cadastrados.

    Returns:
        List[Produto]: Uma lista de objetos de produtos cadastrados.
    """
    return produtos


# # Rota para simular o histórico de compras de um usuário
# @router.post("/historico_compras/{usuario_id}")
# def adicionar_historico_compras(usuario_id: int, compras: HistoricoCompras):
#     historico_compras[usuario_id] = compras.produtos_ids
#     return {"mensagem": "Histórico de compras atualizado"}


@router.post("/historico_compras/{usuario_id}")
def adicionar_historico_compras(usuario_id: int, compras: HistoricoCompras) -> dict:
    """
    Adiciona ou atualiza o histórico de compras de um usuário.

    Args:
        usuario_id (int): O ID do usuário para o qual o histórico de compras será atualizado.
        compras (HistoricoCompras): O objeto contendo os IDs dos produtos comprados.

    Returns:
        dict: Mensagem indicando que o histórico de compras foi atualizado.
    """
    if usuario_id not in [usuario.id for usuario in usuarios]:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    historico_compras[usuario_id] = compras.produtos_ids
    return {"mensagem": "Histórico de compras atualizado"}


@router.post("/recomendacoes/{usuario_id}", response_model=List[Produto])
def recomendar_produtos(usuario_id: int, preferencias: Preferencias) -> List[Produto]:
    """
    Recomenda produtos com base no histórico de compras e preferências do usuário.

    Args:
        usuario_id (int): O ID do usuário para o qual as recomendações serão feitas.
        preferencias (Preferencias): O objeto contendo as preferências do usuário, como categorias e tags.

    Raises:
        HTTPException: Se o histórico de compras não for encontrado para o usuário.

    Returns:
        List[Produto]: Uma lista de produtos recomendados com base no histórico de compras e preferências.
    """
    if usuario_id not in historico_compras:
        print("Histórico de compras não encontrado")
        raise HTTPException(
            status_code=404, detail="Histórico de compras não encontrado"
        )

    produtos_recomendados = []

    # Buscar produtos com base no histórico de compras do usuário
    for produto_id in historico_compras[usuario_id]:
        for produto in produtos:
            if produto.id == produto_id:
                produtos_recomendados.append(produto)

    # produtos_recomendados = [produto for produto_id in historico_compras[usuario_id] for produto in produtos if produto.id == produto_id]
    """
    produtos_recomendados = [
        produto
        for produto_id in historico_compras[usuario_id]
        for produto in produtos
        if produto.id == produto_id
    ]
    """

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
