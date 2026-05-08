# API de Renda Fixa

API REST para gestão de títulos de renda fixa, cadastro de clientes e alocações, construída com **Python + FastAPI**.

## Pré-requisitos

- Docker



## Como executar

### 1. Suba a API com Docker
```bash
docker compose up --build
```
O backend estará disponível em **http://localhost:8000**.

### 2. Front-end simples (opcional)
Para testar a API visualmente, rode na mesma pasta do arquivo index.html:
```bash
python -m http.server 8080
```
Depois, acesse **http://localhost:8080** no navegador para abrir a interface web.

### 3. Documentação interativa
Acesse **http://localhost:8000/docs** para testar e explorar todos os endpoints da API via Swagger UI.

### 4. Encerrar
Para parar a aplicação:
```bash
docker compose down
```


---

## Como funciona

- **Títulos**: Lidos automaticamente do arquivo Excel `taxas_indicativas.xlsm` (abas "Crédito bancário" e "Títulos Públicos").
- **Clientes e alocações**: Mockados em memória, criados via API ou pelo front-end.
- **Front-end**: Interface web simples em `index.html` para cadastrar clientes, listar títulos, alocar títulos e visualizar tudo em tabelas.
- **Documentação**: Todos os endpoints e exemplos de uso estão em `/docs` (Swagger UI), acessível ao rodar a API.

---

---

## Endpoints

| Recurso   | Método | Rota                      | Descrição                     |
|-----------|--------|---------------------------|-------------------------------|
| Títulos   | GET    | `/titulos/`               | Lista com filtros opcionais   |
| Títulos   | GET    | `/titulos/tipos`          | Resumo por tipo de produto    |
| Títulos   | GET    | `/titulos/{id}`           | Detalha um título             |
| Clientes  | POST   | `/clientes/`              | Cadastra cliente              |
| Clientes  | GET    | `/clientes/`              | Lista clientes                |
| Clientes  | GET    | `/clientes/{id}`          | Busca cliente                 |
| Clientes  | DELETE | `/clientes/{id}`          | Remove cliente                |
| Alocações | POST   | `/alocacoes/`             | Aloca título a um cliente     |
| Alocações | GET    | `/alocacoes/`             | Lista alocações               |
| Alocações | GET    | `/alocacoes/cliente/{id}` | Alocações de um cliente       |
| Alocações | GET    | `/alocacoes/{id}`         | Detalha alocação              |
| Alocações | DELETE | `/alocacoes/{id}`         | Remove alocação               |

Filtros em `GET /titulos/`: `produto`, `indexador`, `fonte`, `emissor`, `aplicacao_min`.

**Perfis aceitos:** `conservador`, `moderado`, `arrojado`

---

## Exemplo de uso

```bash
# Listar CDBs disponíveis
curl http://localhost:8000/titulos/?produto=CDB

# Cadastrar cliente
curl -X POST http://localhost:8000/clientes/ \
  -H "Content-Type: application/json" \
  -d '{"nome":"Ynara Silva","email":"ynara@email.com","cpf":"12345678900","perfil":"moderado"}'

# Alocar título ao cliente
curl -X POST http://localhost:8000/alocacoes/ \
  -H "Content-Type: application/json" \
  -d '{"cliente_id":1,"titulo_id":5,"valor":5000}'
```

---

## Testes

```bash
pip install -r requirements.txt
pytest tests/ -v
```

---

## Decisões técnicas

**Carregamento na inicialização**
O arquivo `.xlsm` é lido uma única vez via `lifespan` do FastAPI. Se o arquivo estiver ausente ou inválido, a aplicação falha no startup com mensagem clara não silenciosamente na primeira requisição.

**Persistência em memória**
Clientes e alocações vivem em um `dataclass AppState` injetado via `Depends`. Substituir por SQLAlchemy + PostgreSQL não exige mudança nos routers: basta trocar a implementação de `get_db`.

**Injeção de dependência**
Routers recebem o estado via `DB = Annotated[AppState, Depends(get_db)]`. Nos testes, a dependência é sobrescrita com uma instância limpa por teste isolamento real, sem mocks frágeis.

**Validação via Pydantic**
O campo `perfil` usa `Literal["conservador", "moderado", "arrojado"]`. FastAPI retorna 422 automaticamente para valores inválidos, sem código manual.

---

## Estrutura

```
├── main.py
├── app/
│   ├── models.py        # Schemas Pydantic
│   ├── state.py         # Estado em memória (clientes, alocações)
│   ├── loader.py        # Leitura do .xlsm
│   ├── dependencies.py  # FastAPI Depends
│   └── routers/
│       ├── titulos.py
│       ├── clientes.py
│       └── alocacoes.py
├── tests/
│   ├── conftest.py      # Fixtures com isolamento por teste
│   └── test_api.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```
