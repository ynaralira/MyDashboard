from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.dependencies import DB
from app.models import Titulo

router = APIRouter()


@router.get("/", response_model=List[Titulo], summary="Lista títulos com filtros opcionais")
def listar_titulos(
    db: DB,
    produto: Optional[str] = Query(None, description="Ex: CDB, LCA, LCI, NTN-B, LTN"),
    indexador: Optional[str] = Query(None, description="Ex: %CDI, IPCA, PRE"),
    fonte: Optional[str] = Query(None, description="bancario | publico"),
    emissor: Optional[str] = Query(None, description="Busca parcial, case-insensitive"),
    aplicacao_min: Optional[float] = Query(None, description="Valor máximo de aplicação mínima"),
):
    result = list(db.titulos.values())

    if produto:
        result = [t for t in result if t.produto.upper() == produto.upper()]
    if indexador:
        result = [t for t in result if indexador.upper() in t.indexador.upper()]
    if fonte:
        result = [t for t in result if t.fonte == fonte]
    if emissor:
        result = [t for t in result if emissor.lower() in t.emissor.lower()]
    if aplicacao_min is not None:
        result = [t for t in result if t.aplicacao_minima is not None and t.aplicacao_minima <= aplicacao_min]

    return result


@router.get("/tipos", summary="Resumo dos tipos de produtos disponíveis")
def listar_tipos(db: DB):
    produtos = sorted({t.produto for t in db.titulos.values()})
    por_fonte: dict = {}
    for t in db.titulos.values():
        por_fonte[t.fonte] = por_fonte.get(t.fonte, 0) + 1
    return {"total": len(db.titulos), "produtos": produtos, "por_fonte": por_fonte}


@router.get("/{titulo_id}", response_model=Titulo, summary="Detalha um título pelo ID")
def detalhar_titulo(titulo_id: int, db: DB):
    titulo = db.titulos.get(titulo_id)
    if not titulo:
        raise HTTPException(status_code=404, detail="Título não encontrado")
    return titulo
