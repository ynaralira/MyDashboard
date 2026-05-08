from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator

Perfil = Literal["conservador", "moderado", "arrojado"]


class Titulo(BaseModel):
    id: int
    emissor: str
    produto: str
    prazo_dias: Optional[int] = None
    vencimento: Optional[str] = None
    indexador: str
    taxa_maxima: Optional[float] = None
    taxa_portal: Optional[float] = None
    spread_portal: Optional[float] = None
    receita_estimada: Optional[float] = None
    aplicacao_minima: Optional[float] = None
    rating: Optional[str] = None
    juros: Optional[str] = None
    fonte: Literal["bancario", "publico"]


class ClienteCreate(BaseModel):
    nome: str
    email: str
    cpf: str
    perfil: Perfil

    @field_validator("cpf")
    @classmethod
    def validate_cpf(cls, v: str) -> str:
        digits = "".join(c for c in v if c.isdigit())
        if len(digits) != 11:
            raise ValueError("CPF deve conter 11 dígitos numéricos")
        return digits


class Cliente(ClienteCreate):
    id: int


class AlocacaoCreate(BaseModel):
    cliente_id: int
    titulo_id: int
    valor: float = Field(gt=0, description="Valor da alocação em R$")


class Alocacao(BaseModel):
    id: int
    cliente_id: int
    titulo_id: int
    valor: float
    emissor: str
    produto: str
    indexador: str
    taxa_portal: Optional[float] = None
    vencimento: Optional[str] = None
