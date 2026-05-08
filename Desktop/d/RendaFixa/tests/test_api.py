import pytest
from fastapi.testclient import TestClient

CLIENTE = {
    "nome": "Ynara",
    "email": "ynara@email.com",
    "cpf": "12345678900",
    "perfil": "moderado",
}

def test_root(client: TestClient):
    r = client.get("/")
    assert r.status_code == 200
    assert "docs" in r.json()

def test_listar_titulos(client: TestClient):
    r = client.get("/titulos/")
    assert r.status_code == 200
    assert len(r.json()) > 0


def test_filtro_por_produto(client: TestClient):
    r = client.get("/titulos/?produto=CDB")
    assert r.status_code == 200
    assert all(t["produto"] == "CDB" for t in r.json())


def test_filtro_por_fonte_publico(client: TestClient):
    r = client.get("/titulos/?fonte=publico")
    assert r.status_code == 200
    assert all(t["fonte"] == "publico" for t in r.json())


def test_listar_tipos(client: TestClient):
    r = client.get("/titulos/tipos")
    assert r.status_code == 200
    data = r.json()
    assert "produtos" in data
    assert "CDB" in data["produtos"]


def test_detalhar_titulo(client: TestClient):
    r = client.get("/titulos/1")
    assert r.status_code == 200
    assert r.json()["id"] == 1


def test_titulo_nao_encontrado(client: TestClient):
    assert client.get("/titulos/999999").status_code == 404


def test_criar_cliente(client: TestClient):
    r = client.post("/clientes/", json=CLIENTE)
    assert r.status_code == 201
    data = r.json()
    assert data["nome"] == CLIENTE["nome"]
    assert "id" in data


def test_cpf_duplicado(client: TestClient):
    client.post("/clientes/", json=CLIENTE)
    r = client.post("/clientes/", json=CLIENTE)
    assert r.status_code == 409


def test_perfil_invalido(client: TestClient):
    r = client.post("/clientes/", json={**CLIENTE, "perfil": "nerd"})
    assert r.status_code == 422


def test_listar_clientes(client: TestClient):
    client.post("/clientes/", json=CLIENTE)
    r = client.get("/clientes/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_cliente_nao_encontrado(client: TestClient):
    assert client.get("/clientes/999999").status_code == 404


def _criar_cliente(client: TestClient) -> int:
    r = client.post("/clientes/", json=CLIENTE)
    return r.json()["id"]


def test_criar_alocacao(client: TestClient):
    cliente_id = _criar_cliente(client)
    titulos = client.get("/titulos/").json()
    titulo = titulos[0]
    valor = titulo["aplicacao_minima"] or 100.0

    r = client.post("/alocacoes/", json={
        "cliente_id": cliente_id,
        "titulo_id": titulo["id"],
        "valor": valor,
    })
    assert r.status_code == 201
    assert r.json()["cliente_id"] == cliente_id


def test_alocacao_valor_abaixo_minimo(client: TestClient):
    cliente_id = _criar_cliente(client)
    titulos = client.get("/titulos/?produto=CDB").json()
    titulo = next((t for t in titulos if (t["aplicacao_minima"] or 0) > 1), None)
    if titulo is None:
        pytest.skip("Nenhum CDB com aplicação mínima > 1")

    r = client.post("/alocacoes/", json={
        "cliente_id": cliente_id,
        "titulo_id": titulo["id"],
        "valor": 0.01,
    })
    assert r.status_code == 422


def test_alocacao_cliente_inexistente(client: TestClient):
    titulos = client.get("/titulos/").json()
    r = client.post("/alocacoes/", json={
        "cliente_id": 999999,
        "titulo_id": titulos[0]["id"],
        "valor": 1000.0,
    })
    assert r.status_code == 404


def test_listar_alocacoes(client: TestClient):
    assert client.get("/alocacoes/").status_code == 200


def test_alocacoes_por_cliente_inexistente(client: TestClient):
    assert client.get("/alocacoes/cliente/999999").status_code == 404
