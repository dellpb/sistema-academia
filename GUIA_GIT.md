# Guia de Git (VS Code) – o que fazer na sua parte

Substitua `<URL>` pelo link do repositório do grupo.

## 1. Atualizar o repositório
```bash
git clone <URL>        # ou, se já tem: git pull origin main
cd nome-do-repo
```

## 2. Criar sua branch
```bash
git checkout -b feature/estrutura-academia
```

## 3. Copiar os arquivos do projeto para dentro da pasta do repositório
Se o seu parceiro já criou arquivos com os mesmos nomes, combinem qual versão manter.

## 4. Fazer commits pequenos e separados (todos com sua autoria)
```bash
git add models/ && git commit -m "feat: adiciona modelos Aluno, Plano e Matricula"
git add utils/ && git commit -m "feat: adiciona validacoes de CPF, telefone e valores"
git add services/ && git commit -m "feat: implementa servico de academia e persistencia JSON"
git add main.py && git commit -m "feat: adiciona menu interativo"
git add tests/ && git commit -m "test: adiciona testes automatizados"
git add README.md GUIA_GIT.md .gitignore requirements.txt data/.gitkeep && git commit -m "docs: adiciona README e configuracoes"
```

## 5. Enviar e abrir Pull Request
```bash
git push -u origin feature/estrutura-academia
```
No GitHub: **Compare & pull request** → peça ao parceiro para revisar e fazer o **merge** na `main`.

## 6. Conferir antes de entregar
- Seu parceiro e você aparecem nos commits.
- README com os nomes reais do grupo.
- Link do repositório aberto em aba anônima.
- Entregar o link na plataforma até 04/12/2026, 23:59.
