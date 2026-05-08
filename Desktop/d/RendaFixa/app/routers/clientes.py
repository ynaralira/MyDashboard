from fastapi import APIRouter, HTTPException
from typing import List
from app.dependencies import DB
from app.models import Cliente, ClienteCreate

router = APIRouter()


@router.post("/", response_model=Cliente, status_code=201, summary="Cadastra um novo cliente")
def criar_cliente(cliente: ClienteCreate, db: DB):
    if any(c.cpf == cliente.cpf for c in db.clientes.values()):
        raise HTTPException(status_code=409, detail="CPF já cadastrado")

    novo_id = db.next_cliente_id()
    novo = Cliente(id=novo_id, **cliente.model_dump())
    db.clientes[novo_id] = novo
    return novo


@router.get("/", response_model=List[Cliente], summary="Lista todos os clientes")
def listar_clientes(db: DB):
    return list(db.clientes.values())


@router.get("/{cliente_id}", response_model=Cliente, summary="Busca um cliente pelo ID")
def buscar_cliente(cliente_id: int, db: DB):
    cliente = db.clientes.get(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente


@router.delete("/{cliente_id}", status_code=204, summary="Remove um cliente")
def remover_cliente(cliente_id: int, db: DB):
    if cliente_id not in db.clientes:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    del db.clientes[cliente_id]
