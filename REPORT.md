# REPORT — Sistema Biblioteca (FastAPI + SQLite)

## Arquitetura
- Frontend: HTML5, CSS3, JavaScript (ES6) — pasta `frontend/`
- Backend: FastAPI + SQLite (sqlite3) — pasta `backend/`
- Banco: arquivo `backend/biblioteca.db`

Fluxo:
1) Browser → JS (fetch) → `http://localhost:8000/*`
2) FastAPI (`backend/app.py`) → sqlite3 → `biblioteca.db`
3) Resposta JSON → Frontend renderiza cards e ações

## Tecnologias e versões
- Python 3.13
- FastAPI + Uvicorn
- SQLite (sqlite3 nativo)
- VS Code + Thunder Client/REST Client

## Endpoints implementados
- GET `/livros?search=&genero=&ano=&status=`
- POST `/livros`
- PUT `/livros/{id}`
- DELETE `/livros/{id}`
- POST `/livros/{id}/emprestar`
- POST `/livros/{id}/devolver`
- GET `/health`

## Peculiaridades (3 de 10)
- Filtro avançado (gênero + ano + texto) sem recarregar
- Ordenação persistida (localStorage)
- Exportação CSV/JSON da lista atual
- Bônus: Atalhos acessíveis (Alt+N), foco visível, aria-* nos elementos principais

## Validações
- Frontend: título obrigatório (3–90), ano 1900–atual, impedimento de título duplicado local, URL de capa opcional.
- Backend: ano válido; impedimento de empréstimo quando status=emprestado; devolver só quando status!=disponível; título único (constraint + erro 400).

## Acessibilidade
- Cores com contraste ≥ 4.5:1; foco visível; aria-label na busca; aria-live na listagem.

## Como rodar
1. Backend
```
cd backend
python -m uvicorn app:app --reload
python .\seed.py  # popular ~20 livros
```
2. Frontend (opção simples)
```
cd frontend
python -m http.server 5500
```
3. Teste
- http://127.0.0.1:8000/docs
- http://localhost:5500

## Prints
- [x] Home com cards
- [x] Health 200 e /livros com itens

## Limitações e melhorias
- Sem autenticação/usuários.
- Falta paginação no backend (front faz fatia local).
- Possível adicionar tema claro/escuro e testes automatizados.
- Dependências legadas em requirements.txt (SQLAlchemy) não usadas.


## Prompts do Copilot (resumo)
- “Gerar HTML com header, filtros e modais…"
- “Atualizar CSS para paleta #1E3A8A/#F59E0B/#10B981…"
- “JS: CRUD via fetch + filtros/ordenação/paginação…”
- “FastAPI + sqlite3: CRUD + emprestar/devolver + validações…”
- “Seed com 20 livros plausíveis…”
- “Ajustes CORS e base URL para frontend file:// …”

> Observação: alguns trechos foram ajustados manualmente para simplicidade e compatibilidade em aula.
