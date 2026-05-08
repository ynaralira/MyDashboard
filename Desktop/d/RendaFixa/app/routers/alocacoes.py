from fastapi import APIRouter, HTTPException
from typing import List
from app.dependencies import DB
from app.models import Alocacao, AlocacaoCreate

router = APIRouter()


@router.post("/", response_model=Alocacao, status_code=201, summary="Aloca um título para um cliente")
def criar_alocacao(alocacao: AlocacaoCreate, db: DB):
    if alocacao.cliente_id not in db.clientes:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    titulo = db.titulos.get(alocacao.titulo_id)
    if not titulo:
        raise HTTPException(status_code=404, detail="Título não encontrado")

    if titulo.aplicacao_minima and alocacao.valor < titulo.aplicacao_minima:
        raise HTTPException(
            status_code=422,
            detail=f"Valor mínimo de aplicação é R$ {titulo.aplicacao_minima:,.2f}",
        )

    novo_id = db.next_alocacao_id()
    nova = Alocacao(
        id=novo_id,
        cliente_id=alocacao.cliente_id,
        titulo_id=alocacao.titulo_id,
        valor=alocacao.valor,
        emissor=titulo.emissor,
        produto=titulo.produto,
        indexador=titulo.indexador,
        taxa_portal=titulo.taxa_portal,
        vencimento=titulo.vencimento,
    )
    db.alocacoes[novo_id] = nova
    return nova


@router.get("/", response_model=List[Alocacao], summary="Lista todas as alocações")
def listar_alocacoes(db: DB):
    return list(db.alocacoes.values())


@router.get("/cliente/{cliente_id}", response_model=List[Alocacao], summary="Alocações de um cliente")
def alocacoes_por_cliente(cliente_id: int, db: DB):
    if cliente_id not in db.clientes:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return [a for a in db.alocacoes.values() if a.cliente_id == cliente_id]


@router.get("/{alocacao_id}", response_model=Alocacao, summary="Detalha uma alocação")
def detalhar_alocacao(alocacao_id: int, db: DB):
    alocacao = db.alocacoes.get(alocacao_id)
    if not alocacao:
        raise HTTPException(status_code=404, detail="Alocação não encontrada")
    return alocacao


@router.delete("/{alocacao_id}", status_code=204, summary="Remove uma alocação")
def remover_alocacao(alocacao_id: int, db: DB):
    if alocacao_id not in db.alocacoes:
        raise HTTPException(status_code=404, detail="Alocação não encontrada")
    del db.alocacoes[alocacao_id]
