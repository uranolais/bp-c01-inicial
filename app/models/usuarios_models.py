from pydantic import BaseModel

# Modelo base para um usuário
class Usuario(BaseModel):
    """
    Modelo para um usuário.

    Attributes:
        id (int): O identificador único do usuário.
        nome (str): O nome do usuário.
    """
    id: int
    nome: str