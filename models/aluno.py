from dataclasses import dataclass, asdict


@dataclass
class Aluno:
    id: int
    nome: str
    cpf: str
    telefone: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, dados: dict) -> "Aluno":
        return cls(**dados)
