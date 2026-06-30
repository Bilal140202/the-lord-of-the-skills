---
trigger: always_on
---

# Constituição do Projeto TodoApp

## Arquitetura Obrigatória
- Padrão: MVC com Flask Blueprints
- Proibido: lógica de negócio nas rotas (vai nos services/)
- Proibido: SQL raw (usar SQLAlchemy ORM)

## Módulos Obrigatórios
- auth/       → Blueprint de autenticação
- tasks/      → Blueprint de tarefas (CRUD)
- models/     → Entidades SQLAlchemy
- templates/  → HTML Jinja2

## Critérios de Aceitação Globais
- Todo endpoint autenticado retorna 401 se não logado
- Tarefas pertencem ao usuário — nunca expor tarefas de outros
- Todos os formulários com proteção CSRF
- Cobertura de testes: mínimo 80%