"""Regras de negócio da academia."""
import os
from datetime import date

from models.aluno import Aluno
from models.plano import Plano
from models.matricula import Matricula, ATIVA, CANCELADA
from services.storage import RepositorioJSON
from utils.validacoes import (
    ErroNegocio, validar_nome, validar_cpf, validar_telefone,
    validar_valor, validar_inteiro_positivo, somar_meses,
)


class AcademiaService:
    def __init__(self, pasta_dados: str = "data"):
        self._repo_alunos = RepositorioJSON(os.path.join(pasta_dados, "alunos.json"))
        self._repo_planos = RepositorioJSON(os.path.join(pasta_dados, "planos.json"))
        self._repo_matriculas = RepositorioJSON(os.path.join(pasta_dados, "matriculas.json"))

        self.alunos = [Aluno.from_dict(d) for d in self._repo_alunos.carregar()]
        self.planos = [Plano.from_dict(d) for d in self._repo_planos.carregar()]
        self.matriculas = [Matricula.from_dict(d) for d in self._repo_matriculas.carregar()]

    # ---------- utilitários internos ----------
    @staticmethod
    def _proximo_id(itens: list) -> int:
        return max((i.id for i in itens), default=0) + 1

    def _salvar(self) -> None:
        self._repo_alunos.salvar([a.to_dict() for a in self.alunos])
        self._repo_planos.salvar([p.to_dict() for p in self.planos])
        self._repo_matriculas.salvar([m.to_dict() for m in self.matriculas])

    # ---------- ALUNOS (CRUD) ----------
    def cadastrar_aluno(self, nome: str, cpf: str, telefone: str) -> Aluno:
        nome = validar_nome(nome)
        cpf = validar_cpf(cpf)
        telefone = validar_telefone(telefone)
        if any(a.cpf == cpf for a in self.alunos):
            raise ErroNegocio("Já existe um aluno com esse CPF.")
        aluno = Aluno(self._proximo_id(self.alunos), nome, cpf, telefone)
        self.alunos.append(aluno)
        self._salvar()
        return aluno

    def buscar_aluno(self, aluno_id: int) -> Aluno:
        for aluno in self.alunos:
            if aluno.id == aluno_id:
                return aluno
        raise ErroNegocio("Aluno não encontrado.")

    def listar_alunos(self) -> list:
        return list(self.alunos)

    def atualizar_aluno(self, aluno_id: int, nome: str = None, telefone: str = None) -> Aluno:
        aluno = self.buscar_aluno(aluno_id)
        if nome:
            aluno.nome = validar_nome(nome)
        if telefone:
            aluno.telefone = validar_telefone(telefone)
        self._salvar()
        return aluno

    def remover_aluno(self, aluno_id: int) -> None:
        aluno = self.buscar_aluno(aluno_id)
        if any(m.aluno_id == aluno_id and m.status == ATIVA for m in self.matriculas):
            raise ErroNegocio("Não é possível remover aluno com matrícula ativa.")
        self.alunos.remove(aluno)
        self._salvar()

    # ---------- PLANOS (CRUD) ----------
    def cadastrar_plano(self, nome: str, valor_mensal, duracao_meses) -> Plano:
        nome = validar_nome(nome)
        valor = validar_valor(valor_mensal)
        duracao = validar_inteiro_positivo(duracao_meses, "Duração")
        if any(p.nome.lower() == nome.lower() for p in self.planos):
            raise ErroNegocio("Já existe um plano com esse nome.")
        plano = Plano(self._proximo_id(self.planos), nome, valor, duracao)
        self.planos.append(plano)
        self._salvar()
        return plano

    def buscar_plano(self, plano_id: int) -> Plano:
        for plano in self.planos:
            if plano.id == plano_id:
                return plano
        raise ErroNegocio("Plano não encontrado.")

    def listar_planos(self) -> list:
        return list(self.planos)

    def atualizar_plano(self, plano_id: int, nome: str = None,
                        valor_mensal=None, duracao_meses=None) -> Plano:
        plano = self.buscar_plano(plano_id)
        if nome:
            plano.nome = validar_nome(nome)
        if valor_mensal not in (None, ""):
            plano.valor_mensal = validar_valor(valor_mensal)
        if duracao_meses not in (None, ""):
            plano.duracao_meses = validar_inteiro_positivo(duracao_meses, "Duração")
        self._salvar()
        return plano

    def remover_plano(self, plano_id: int) -> None:
        plano = self.buscar_plano(plano_id)
        if any(m.plano_id == plano_id and m.status == ATIVA for m in self.matriculas):
            raise ErroNegocio("Não é possível remover plano com matrículas ativas.")
        self.planos.remove(plano)
        self._salvar()

    # ---------- MATRÍCULAS ----------
    def matricular(self, aluno_id: int, plano_id: int, inicio: date = None) -> Matricula:
        aluno = self.buscar_aluno(aluno_id)
        plano = self.buscar_plano(plano_id)
        if any(m.aluno_id == aluno.id and m.status == ATIVA for m in self.matriculas):
            raise ErroNegocio("O aluno já possui uma matrícula ativa.")
        inicio = inicio or date.today()
        fim = somar_meses(inicio, plano.duracao_meses)
        matricula = Matricula(self._proximo_id(self.matriculas), aluno.id, plano.id,
                              inicio.isoformat(), fim.isoformat(), ATIVA)
        self.matriculas.append(matricula)
        self._salvar()
        return matricula

    def cancelar_matricula(self, matricula_id: int) -> Matricula:
        for matricula in self.matriculas:
            if matricula.id == matricula_id:
                if matricula.status == CANCELADA:
                    raise ErroNegocio("Matrícula já está cancelada.")
                matricula.status = CANCELADA
                self._salvar()
                return matricula
        raise ErroNegocio("Matrícula não encontrada.")

    def listar_matriculas(self, apenas_ativas: bool = False) -> list:
        if apenas_ativas:
            return [m for m in self.matriculas if m.status == ATIVA]
        return list(self.matriculas)

    # ---------- RELATÓRIO ----------
    def relatorio(self) -> dict:
        ativas = self.listar_matriculas(apenas_ativas=True)
        receita = sum(self.buscar_plano(m.plano_id).valor_mensal for m in ativas)
        return {
            "total_alunos": len(self.alunos),
            "total_planos": len(self.planos),
            "matriculas_ativas": len(ativas),
            "matriculas_canceladas": len(self.matriculas) - len(ativas),
            "receita_mensal": round(receita, 2),
        }
