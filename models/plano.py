from dataclasses import dataclass, asdict


@dataclass
class Plano:
    id: int
    nome: str
    valor_mensal: float
    duracao_meses: int

    @property
    def valor_total(self) -> float:
        return round(self.valor_mensal * self.duracao_meses, 2)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, dados: dict) -> "Plano":
        return cls(**dados)
