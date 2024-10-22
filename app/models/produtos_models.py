from pydantic import BaseModel
from typing import List

# Modelo base para produto
class ProdutoBase(BaseModel):
    """
    Modelo base para um produto.

    Attributes:
        nome (str): O nome do produto.
        categoria (str): A categoria à qual o produto pertence.
        tags (List[str]): Uma lista de tags associadas ao produto.
    """
    nome: str
    categoria: str
    tags: List[str]

# Modelo para criar um produto
class CriarProduto(ProdutoBase):
    """
    Modelo para criar um novo produto.

    Herda todos os atributos do ProdutoBase.
    """
    pass

# Modelo de produto com ID
class Produto(ProdutoBase):
    """
    Modelo para um produto com ID.

    Attributes:
        id (int): O identificador único do produto.
    """
    id: int

# Modelo para histórico de compras do usuário
class HistoricoCompras(BaseModel):
    """
    Modelo para o histórico de compras de um usuário.

    Attributes:
        produtos_ids (List[int]): Uma lista de IDs de produtos comprados pelo usuário.
    """
    produtos_ids: List[int]

# Modelo para preferências do usuário
class Preferencias(BaseModel):
    """
    Modelo para as preferências de um usuário.

    Attributes:
        categorias (List[str] | None): Uma lista de categorias que o usuário prefere. 
        tags (List[str] | None): Uma lista de tags que o usuário prefere. 
                                Ambos podem ser None se não forem especificados.
    """
    categorias: List[str] | None = None
    tags: List[str] | None = None

