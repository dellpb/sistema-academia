from dataclasses import dataclass, asdict

ATIVA = "ativa"
CANCELADA = "cancelada"


@dataclass
class Matricula:
    id: int
    aluno_id: int
    plano_id: int
    data_inicio: str  # formato ISO: AAAA-MM-DD
    data_fim: str
    status: str = ATIVA

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, dados: dict) -> "Matricula":
        return cls(**dados)
