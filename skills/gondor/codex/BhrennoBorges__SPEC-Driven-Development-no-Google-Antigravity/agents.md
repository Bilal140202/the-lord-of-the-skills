# AGENTS.md — TodoApp

## Tech Stack
- Linguagem: Python 3.12
- Framework: Flask com Blueprints (padrão MVC)
- Banco de dados: SQLite via SQLAlchemy ORM (nunca SQL raw)
- Autenticação: Flask-Login + Werkzeug password hash
- Frontend: HTML semântico + Jinja2 + CSS puro
- Testes: pytest, cobertura mínima de 80%

## Regras de Código
- Máximo 300 linhas por arquivo
- Todas as funções exportadas precisam de docstring
- Sem credenciais hardcoded — usar variáveis de ambiente (.env)

## Guardrails de Segurança
- Nunca escrever no banco sem confirmação explícita do usuário
- Nunca fazer deploy sem aprovação humana
- Validar todo input antes de processar

## Git
- Commits co