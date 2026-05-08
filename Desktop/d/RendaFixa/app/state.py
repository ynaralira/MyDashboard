from dataclasses import dataclass, field
from typing import Dict
from app.models import Alocacao, Cliente, Titulo


@dataclass
class AppState:
    titulos: Dict[int, Titulo] = field(default_factory=dict)
    clientes: Dict[int, Cliente] = field(default_factory=dict)
    alocacoes: Dict[int, Alocacao] = field(default_factory=dict)
    cliente_seq: int = field(default=0, repr=False)
    alocacao_seq: int = field(default=0, repr=False)

    def next_cliente_id(self) -> int:
        self.cliente_seq += 1
        return self.cliente_seq

    def next_alocacao_id(self) -> int:
        self.alocacao_seq += 1
        return self.alocacao_seq
