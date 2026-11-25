# Sistema de Gestão de Academia

Projeto Avaliativo AV2 – sistema em Python (terminal) para gerenciar alunos, planos e matrículas de uma academia.

## Integrantes
-  Delosmar Lacerda dos Santos Filho
- Jobson Francisco 
 
## Problema de negócio
Muitas academias pequenas controlam alunos e mensalidades em papel ou planilhas, o que gera
erros, matrículas duplicadas e falta de visão da receita. Este sistema centraliza o cadastro e
aplica regras de negócio automaticamente.

## Funcionalidades
- **Alunos:** cadastrar, listar, atualizar e remover (CPF validado e sem duplicidade).
- **Planos:** cadastrar, listar, atualizar e remover (ex.: Mensal, Trimestral, Anual).
- **Matrículas:** matricular aluno em um plano (data de término calculada), listar e cancelar.
- **Relatório:** total de alunos, matrículas ativas/canceladas e receita mensal.
- **Regras:** aluno só pode ter 1 matrícula ativa; não remove aluno/plano com matrícula ativa.
- **Persistência:** dados salvos em arquivos JSON na pasta `data/`.

## Como executar
Requisito: Python 3.10 ou superior (sem bibliotecas externas).

```bash
python main.py
```

## Como rodar os testes
```bash
python -m unittest discover -s tests -t . -v
```

## Estrutura de pastas
```
sistema_academia/
├── main.py                    # menu interativo
├── models/                    # classes Aluno, Plano, Matricula
├── services/
│   ├── academia_service.py    # regras de negócio (CRUD e relatório)
│   └── storage.py             # persistência em JSON
├── utils/validacoes.py        # validações (CPF, telefone, valores, datas)
├── tests/                     # testes automatizados (unittest)
├── data/                      # arquivos JSON gerados em execução
├── README.md
├── GUIA_GIT.md
└── requirements.txt
```

## Conceitos aplicados
POO (dataclasses), modularização, tratamento de exceções (`ErroNegocio`), validação de entrada,
persistência de dados, testes automatizados e controle de versão com Git (branches e pull requests).
