# FinanceMind

Plataforma de educação e acompanhamento de investimentos para investidores iniciantes e intermediários no Brasil.

Toda a documentação de produto, arquitetura, dados, API, telas, IA, segurança/compliance e roadmap está em [`docs/`](./docs/00-indice.md). Comece por lá.

## Status

Fundação técnica (M0) criada: scaffold de backend e frontend, sem features de negócio ainda implementadas. Próximo passo do roadmap: M1 — Autenticação e Landing Page (ver [`docs/09-backlog-roadmap-sprints.md`](./docs/09-backlog-roadmap-sprints.md)).

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

Requer um PostgreSQL local rodando (ajuste `DATABASE_URL` em `backend/.env`).

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
