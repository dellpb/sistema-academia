import unittest
from datetime import date

from services.academia_service import AcademiaService
from utils.validacoes import ErroNegocio, validar_cpf, somar_meses

CPF1 = "529.982.247-25"
CPF2 = "111.444.777-35"


class TestValidacoes(unittest.TestCase):
    def test_cpf_valido(self):
        self.assertEqual(validar_cpf(CPF1), "52998224725")

    def test_cpf_invalido(self):
        for cpf in ("123", "11111111111", "52998224720"):
            with self.assertRaises(ErroNegocio):
                validar_cpf(cpf)

    def test_somar_meses(self):
        self.assertEqual(somar_meses(date(2026, 1, 31), 1), date(2026, 2, 28))
        self.assertEqual(somar_meses(date(2026, 11, 15), 3), date(2027, 2, 15))


class TestService(unittest.TestCase):
    def setUp(self):
        self.svc = AcademiaService()

    def test_crud_aluno(self):
        a = self.svc.cadastrar_aluno("Maria Silva", CPF1, "11999998888")
        self.svc.atualizar_aluno(a.id, nome="Maria Souza")
        self.assertEqual(self.svc.buscar_aluno(a.id).nome, "Maria Souza")
        self.svc.remover_aluno(a.id)
        self.assertEqual(self.svc.listar_alunos(), [])

    def test_cpf_duplicado(self):
        self.svc.cadastrar_aluno("Maria Silva", CPF1, "11999998888")
        with self.assertRaises(ErroNegocio):
            self.svc.cadastrar_aluno("Outra Pessoa", CPF1, "11999997777")

    def test_matricula_e_regras(self):
        a = self.svc.cadastrar_aluno("João Lima", CPF2, "11988887777")
        p = self.svc.cadastrar_plano("Trimestral", "99,90", 3)
        m = self.svc.matricular(a.id, p.id, date(2026, 11, 24))
        self.assertEqual(m.data_fim, "2027-02-24")
        with self.assertRaises(ErroNegocio):
            self.svc.matricular(a.id, p.id)       # já matriculado
        with self.assertRaises(ErroNegocio):
            self.svc.remover_aluno(a.id)           # matrícula ativa
        with self.assertRaises(ErroNegocio):
            self.svc.remover_plano(p.id)           # plano em uso
        self.assertEqual(self.svc.relatorio()["receita_mensal"], 99.90)
        self.svc.cancelar_matricula(m.id)
        self.assertEqual(self.svc.relatorio()["matriculas_ativas"], 0)
        self.svc.remover_aluno(a.id)

    def test_dados_somente_em_memoria(self):
        self.svc.cadastrar_plano("Mensal", 80, 1)
        novo = AcademiaService()  # nova instância começa vazia
        self.assertEqual(novo.listar_planos(), [])

    def test_plano_invalido(self):
        with self.assertRaises(ErroNegocio):
            self.svc.cadastrar_plano("Teste", "-5", 1)
        with self.assertRaises(ErroNegocio):
            self.svc.cadastrar_plano("Teste", "abc", 1)


if __name__ == "__main__":
    unittest.main()