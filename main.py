"""Sistema de Gestão de Academia - menu de terminal."""
from datetime import date

from services.academia_service import AcademiaService
from utils.validacoes import ErroNegocio, formatar_cpf


def ler_inteiro(mensagem: str) -> int:
    try:
        return int(input(mensagem).strip())
    except ValueError:
        raise ErroNegocio("Digite um número inteiro válido.")


def formatar_data(iso: str) -> str:
    return date.fromisoformat(iso).strftime("%d/%m/%Y")


# ---------- Alunos ----------
def menu_alunos(svc: AcademiaService) -> None:
    while True:
        print("\n--- ALUNOS ---")
        print("1. Cadastrar\n2. Listar\n3. Atualizar\n4. Remover\n0. Voltar")
        opcao = input("Opção: ").strip()
        try:
            if opcao == "1":
                aluno = svc.cadastrar_aluno(input("Nome: "), input("CPF: "), input("Telefone (com DDD): "))
                print(f"Aluno cadastrado com ID {aluno.id}.")
            elif opcao == "2":
                alunos = svc.listar_alunos()
                if not alunos:
                    print("Nenhum aluno cadastrado.")
                for a in alunos:
                    print(f"[{a.id}] {a.nome} | CPF {formatar_cpf(a.cpf)} | Tel {a.telefone}")
            elif opcao == "3":
                aluno_id = ler_inteiro("ID do aluno: ")
                print("Deixe em branco para manter o valor atual.")
                svc.atualizar_aluno(aluno_id, input("Novo nome: "), input("Novo telefone: "))
                print("Aluno atualizado.")
            elif opcao == "4":
                svc.remover_aluno(ler_inteiro("ID do aluno: "))
                print("Aluno removido.")
            elif opcao == "0":
                return
            else:
                print("Opção inválida.")
        except ErroNegocio as erro:
            print(f"Erro: {erro}")


# ---------- Planos ----------
def menu_planos(svc: AcademiaService) -> None:
    while True:
        print("\n--- PLANOS ---")
        print("1. Cadastrar\n2. Listar\n3. Atualizar\n4. Remover\n0. Voltar")
        opcao = input("Opção: ").strip()
        try:
            if opcao == "1":
                plano = svc.cadastrar_plano(input("Nome: "), input("Valor mensal (R$): "),
                                            input("Duração (meses): "))
                print(f"Plano cadastrado com ID {plano.id}.")
            elif opcao == "2":
                planos = svc.listar_planos()
                if not planos:
                    print("Nenhum plano cadastrado.")
                for p in planos:
                    print(f"[{p.id}] {p.nome} | R$ {p.valor_mensal:.2f}/mês | "
                          f"{p.duracao_meses} meses | Total R$ {p.valor_total:.2f}")
            elif opcao == "3":
                plano_id = ler_inteiro("ID do plano: ")
                print("Deixe em branco para manter o valor atual.")
                svc.atualizar_plano(plano_id, input("Novo nome: "),
                                    input("Novo valor mensal: "), input("Nova duração: "))
                print("Plano atualizado.")
            elif opcao == "4":
                svc.remover_plano(ler_inteiro("ID do plano: "))
                print("Plano removido.")
            elif opcao == "0":
                return
            else:
                print("Opção inválida.")
        except ErroNegocio as erro:
            print(f"Erro: {erro}")


# ---------- Matrículas ----------
def menu_matriculas(svc: AcademiaService) -> None:
    while True:
        print("\n--- MATRÍCULAS ---")
        print("1. Matricular aluno\n2. Listar\n3. Cancelar\n0. Voltar")
        opcao = input("Opção: ").strip()
        try:
            if opcao == "1":
                m = svc.matricular(ler_inteiro("ID do aluno: "), ler_inteiro("ID do plano: "))
                print(f"Matrícula {m.id} criada. Válida até {formatar_data(m.data_fim)}.")
            elif opcao == "2":
                matriculas = svc.listar_matriculas()
                if not matriculas:
                    print("Nenhuma matrícula registrada.")
                for m in matriculas:
                    aluno = svc.buscar_aluno(m.aluno_id).nome if any(
                        a.id == m.aluno_id for a in svc.alunos) else "(removido)"
                    plano = svc.buscar_plano(m.plano_id).nome if any(
                        p.id == m.plano_id for p in svc.planos) else "(removido)"
                    print(f"[{m.id}] {aluno} | {plano} | {formatar_data(m.data_inicio)} a "
                          f"{formatar_data(m.data_fim)} | {m.status}")
            elif opcao == "3":
                svc.cancelar_matricula(ler_inteiro("ID da matrícula: "))
                print("Matrícula cancelada.")
            elif opcao == "0":
                return
            else:
                print("Opção inválida.")
        except ErroNegocio as erro:
            print(f"Erro: {erro}")


def mostrar_relatorio(svc: AcademiaService) -> None:
    r = svc.relatorio()
    print("\n--- RELATÓRIO ---")
    print(f"Alunos cadastrados:    {r['total_alunos']}")
    print(f"Planos cadastrados:    {r['total_planos']}")
    print(f"Matrículas ativas:     {r['matriculas_ativas']}")
    print(f"Matrículas canceladas: {r['matriculas_canceladas']}")
    print(f"Receita mensal:        R$ {r['receita_mensal']:.2f}")


def main() -> None:
    svc = AcademiaService()
    while True:
        print("\n===== SISTEMA DE ACADEMIA =====")
        print("1. Alunos\n2. Planos\n3. Matrículas\n4. Relatório\n0. Sair")
        opcao = input("Opção: ").strip()
        if opcao == "1":
            menu_alunos(svc)
        elif opcao == "2":
            menu_planos(svc)
        elif opcao == "3":
            menu_matriculas(svc)
        elif opcao == "4":
            mostrar_relatorio(svc)
        elif opcao == "0":
            print("Até logo!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nEncerrado.")
