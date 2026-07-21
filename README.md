# FinanceMind

Plataforma de educação e acompanhamento de investimentos para investidores iniciantes e intermediários no Brasil.

Toda a documentação de produto, arquitetura, dados, API, telas, IA, segurança/compliance e roadmap está em [`docs/`](./docs/00-indice.md). Comece por lá.

## Status

- **M0 — Fundação técnica**: concluído. Scaffold de backend e frontend.
- **M1 — Autenticação e Landing Page**: concluído. Registro/login (email+senha), login com Google, refresh/logout, recuperação de senha, verificação de email (todos com testes automatizados no backend) e landing page completa (Hero, Sobre, Benefícios, Recursos, Planos, Depoimentos, FAQ, Contato).

Próximo passo do roadmap: **M2 — Carteira** (catálogo de ativos via brapi.dev/BACEN/Tesouro Transparente + lançamento de transações). Ver [`docs/09-backlog-roadmap-sprints.md`](./docs/09-backlog-roadmap-sprints.md).

**Pendências antes de produção real**: preencher `GOOGLE_CLIENT_ID`/`GOOGLE_CLIENT_SECRET` e `RESEND_API_KEY` no `.env` (sem eles, login Google falha e emails só são logados no console); trocar `JWT_SECRET_KEY` por um valor forte gerado aleatoriamente; os depoimentos da landing page são placeholders — substituir por relatos reais antes do lançamento.

## Rodando localmente

### Opção 1 — Docker Compose (requer Docker instalado)

```bash
cp .env.example .env
docker compose up --build
```

- Backend: http://localhost:8000/api/v1/health
- Frontend: http://localhost:5173

### Opção 2 — Nativo (sem Docker)

**Backend**

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Requer um PostgreSQL local rodando (ajuste `DATABASE_URL` em `backend/.env`). Para rodar os testes (usam SQLite em memória, não precisam de Postgres): `pytest` dentro de `backend/` com o venv ativo.

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

## Estrutura

```
financeMind/
├── docs/         # Documentação completa do projeto
├── backend/      # FastAPI + SQLAlchemy + Alembic
└── frontend/     # Vue 3 + TypeScript + Vuetify + Pinia
```
