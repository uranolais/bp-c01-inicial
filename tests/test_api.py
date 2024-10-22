import pytest
from fastapi.testclient import TestClient
from app.main import app  # Supondo que a instância do FastAPI esteja em main.py

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"mensagem": "Bem-vindo à API de Recomendação de Produtos"}

def test_criar_produto():
    response = client.post("/produtos/", json={"nome": "Produto A", "categoria": "Categoria 1", "tags": ["tag1", "tag2"]})
    assert response.status_code == 200
    assert response.json()["nome"] == "Produto A"

def test_listar_produtos():
    client.post("/produtos/", json={"nome": "Produto B", "categoria": "Categoria 2", "tags": ["tag3"]})
    response = client.get("/produtos/")
    assert response.status_code == 200
    assert len(response.json()) == 2  # Deve ter 2 produtos agora

def test_criar_usuario():
    # Faz a requisição para criar um novo usuário
    response = client.post("/usuarios/", params={"nome": "Usuário Teste"})
    
    # Verifica se o status code da resposta é 200 (sucesso)
    assert response.status_code == 200
    
    # Verifica se a resposta contém o usuário criado corretamente
    usuario_data = response.json()
    
    # Verifica se os campos do usuário estão presentes e corretos
    assert usuario_data["id"] == 1  # Espera-se que o ID seja 1, já que este é o primeiro usuário
    assert usuario_data["nome"] == "Usuário Teste"

def test_adicionar_historico_compras():
    # # Primeiro, cria um usuário sem especificar o ID
    # response_usuario = client.post("/usuarios/", params={"nome": "Usuário 1"})
    # assert response_usuario.status_code == 200  # Confirma que o usuário foi criado com sucesso
    
    # # Agora, cria um produto
    # response_produto = client.post("/produtos/", json={"nome": "Produto 1", "categoria": "Categoria 1", "tags": ["tag1"]})
    # assert response_produto.status_code == 200  # Confirma que o produto foi criado com sucesso
    
    # Agora, adiciona o histórico de compras para o usuário criado
    response = client.post("/historico_compras/1", json={"produtos_ids": [1]})
    assert response.status_code == 200  # Verifica se a requisição foi bem-sucedida
    assert response.json() == {"mensagem": "Histórico de compras atualizado"}  # Verifica a resposta da API

def test_recomendar_produtos():
    client.post("/produtos/", json={"nome": "Produto C", "categoria": "Categoria 1", "tags": ["tag1"]})
    client.post("/historico_compras/1", json={"produtos_ids": [1]})
    response = client.post("/recomendacoes/1", json={"categorias": ["Categoria 1"], "tags": []})
    assert response.status_code == 200
    assert len(response.json()) == 1  # Deveria retornar 1 produto recomendado
