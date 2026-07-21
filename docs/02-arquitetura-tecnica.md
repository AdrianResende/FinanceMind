# 2. Arquitetura Técnica

## 2.1 Stack

| Camada | Tecnologia |
|---|---|
| Frontend | Vue 3 (Composition API) + TypeScript + Pinia + Vue Router + Vuetify 3 + ApexCharts + Axios + vue-i18n |
| Backend | Python 3.12 + FastAPI + Pydantic v2 |
| ORM / Migrations | SQLAlchemy 2.0 (async) + Alembic |
| Banco de dados | PostgreSQL (Docker local em dev, Supabase em produção) |
| Autenticação | JWT (access + refresh) + OAuth2 Google |
| Cache / Jobs | Redis (cache de cotações + fila de jobs com APScheduler ou Celery leve) |
| IA — Chat | LangChain + Groq API (Llama 3.x), camada de abstração de provider |
| IA — Previsão | scikit-learn (Random Forest) + pandas + joblib (persistência de modelo) |
| Dados de mercado | brapi.dev (B3), BACEN SGS (CDI/IPCA/Selic), Tesouro Transparente (Tesouro Direto) |
| Pagamentos | Stripe (Checkout + Billing + Webhooks) |
| Email transacional | Resend |
| Deploy (futuro) | Vercel (frontend) · Railway/Render (backend) · Supabase (Postgres) |
| Versionamento | GitHub, Git Flow simplificado (main + feature branches) |

## 2.2 Visão de containers (C4 — nível 2)

```mermaid
flowchart TB
    subgraph Client["Navegador do Usuário"]
        SPA["Vue 3 SPA (Vuetify + Pinia)"]
    end

    subgraph Backend["FinanceMind API (FastAPI)"]
        API["REST API"]
        AUTH["Módulo Auth (JWT/OAuth2)"]
        PORT["Módulo Carteira"]
        MKT["Módulo Mercado"]
        AI_CHAT["Módulo IA Chat (LangChain + Groq)"]
        AI_ML["Módulo IA Previsão (Random Forest)"]
        BILL["Módulo Billing (Stripe)"]
        JOBS["Scheduler (sync diário de preços/indicadores)"]
    end

    DB[(PostgreSQL)]
    CACHE[(Redis)]

    subgraph External["Serviços Externos"]
        BRAPI["brapi.dev"]
        BACEN["BACEN SGS"]
        TESOURO["Tesouro Transparente"]
        GROQ["Groq API"]
        GOOGLE["Google OAuth"]
        STRIPE["Stripe"]
        RESEND["Resend"]
    end

    SPA -->|HTTPS/JSON| API
    API --> AUTH
    API --> PORT
    API --> MKT
    API --> AI_CHAT
    API --> AI_ML
    API --> BILL

    AUTH --> GOOGLE
    AUTH --> DB
    PORT --> DB
    MKT --> DB
    MKT --> CACHE
    AI_CHAT --> GROQ
    AI_CHAT --> DB
    AI_ML --> DB
    BILL --> STRIPE
    API --> RESEND

    JOBS --> BRAPI
    JOBS --> BACEN
    JOBS --> TESOURO
    JOBS --> DB
    JOBS --> CACHE
```

## 2.3 Fluxo de sincronização de dados de mercado

Job agendado (diário, após fechamento do pregão) que popula o histórico de preços e indicadores usados pelo dashboard e pelo modelo de ML.

```mermaid
sequenceDiagram
    participant S as Scheduler (APScheduler)
    participant J as Job de Sincronização
    participant BR as brapi.dev
    participant BC as BACEN SGS
    participant TS as Tesouro Transparente
    participant DB as PostgreSQL
    participant R as Redis (cache)

    S->>J: Dispara job diário (ex: 19h)
    J->>BR: Busca cotações do dia (ativos ativos na base)
    BR-->>J: Preços de fechamento
    J->>BC: Busca CDI/IPCA/Selic do dia
    BC-->>J: Séries atualizadas
    J->>TS: Busca preços/taxas Tesouro Direto
    TS-->>J: Preços atualizados
    J->>DB: Upsert em asset_price_history / benchmark_history
    J->>R: Invalida cache de cotações
```

## 2.4 Fluxo de autenticação

```mermaid
sequenceDiagram
    participant U as Usuário
    participant F as Frontend (Vue)
    participant A as API Auth
    participant G as Google OAuth
    participant DB as PostgreSQL

    alt Login Email/Senha
        U->>F: Informa email + senha
        F->>A: POST /auth/login
        A->>DB: Verifica hash da senha (argon2)
        DB-->>A: OK
        A-->>F: access_token (15min) + refresh_token (7d, httpOnly cookie)
    else Login Google
        U->>F: Clica em "Entrar com Google"
        F->>G: Redireciona para consentimento OAuth2
        G-->>F: Callback com auth code
        F->>A: POST /auth/google/callback (code)
        A->>G: Troca code por perfil do usuário
        A->>DB: Cria/atualiza usuário vinculado à conta Google
        A-->>F: access_token + refresh_token
    end
    F->>A: Requisições subsequentes com Authorization: Bearer access_token
    A->>A: Middleware valida token e plano do usuário
```

## 2.5 Fluxo do Chat de IA

```mermaid
sequenceDiagram
    participant U as Usuário
    participant F as Frontend
    participant A as API (/ai/chat)
    participant L as LangChain Orchestrator
    participant GQ as Groq LLM
    participant DB as PostgreSQL

    U->>F: Envia pergunta no chat
    F->>A: POST /ai/chat {conversation_id, message}
    A->>DB: Verifica limite de uso do plano (rate limit)
    A->>DB: Carrega histórico da conversa
    A->>L: Monta prompt (system prompt + guardrails + histórico)
    L->>GQ: Chamada ao modelo Llama via Groq
    GQ-->>L: Resposta
    L-->>A: Resposta formatada + disclaimer padrão
    A->>DB: Persiste pergunta e resposta
    A-->>F: Retorna resposta
```

## 2.6 Fluxo da Previsão de ML (Fase 2)

```mermaid
sequenceDiagram
    participant U as Usuário
    participant F as Frontend
    participant A as API (/ai/predict)
    participant M as Serviço ML (Random Forest)
    participant DB as PostgreSQL

    U->>F: Seleciona ativo elegível e clica em "Gerar previsão"
    F->>A: POST /ai/predict {ticker}
    A->>DB: Verifica plano/permite acesso (feature Premium)
    A->>M: Solicita inferência
    M->>DB: Busca histórico de preços (1-2 anos)
    M->>M: Feature engineering (retornos, médias móveis, RSI, volatilidade)
    M->>M: Inferência com modelo treinado (joblib)
    M-->>A: {probabilidade_alta, confiança, features_usadas}
    A-->>F: Resultado + disclaimers obrigatórios
```

## 2.7 Ambientes

- **Desenvolvimento local**: Docker Compose orquestrando `backend` (FastAPI + Uvicorn reload), `frontend` (Vite dev server), `postgres`, `redis`. Variáveis sensíveis via `.env` (nunca commitado).
- **Produção (futuro)**: Frontend estático/SSR-lite no Vercel; backend no Railway ou Render (container Docker); banco no Supabase (Postgres gerenciado); Redis gerenciado (Upstash ou add-on do provedor).
- **CI**: GitHub Actions rodando lint + testes a cada PR (a ser configurado quando o deploy real for priorizado, conforme decidido).

## 2.8 Camada de abstração de LLM (importante para troca futura)

O módulo de IA Chat não deve chamar a API da Groq diretamente do controller. Deve existir uma interface `LLMProvider` (padrão Strategy) com implementação `GroqProvider` hoje, permitindo adicionar `OpenAIProvider`, `AnthropicProvider` ou `GeminiProvider` no futuro apenas trocando a implementação injetada, sem alterar a lógica de negócio do chat (histórico, rate limit, persistência, disclaimers).

## 2.9 Estrutura de pastas

```
financeMind/
├── docs/                          # Esta documentação
├── backend/
│   ├── app/
│   │   ├── main.py                # Entry point FastAPI
│   │   ├── core/                  # Config, segurança, JWT, exceptions
│   │   ├── db/                    # Sessão SQLAlchemy, base declarativa
│   │   ├── models/                # Modelos SQLAlchemy (um arquivo por entidade)
│   │   ├── schemas/                # Schemas Pydantic (request/response)
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── auth.py
│   │   │       ├── users.py
│   │   │       ├── portfolio.py
│   │   │       ├── market.py
│   │   │       ├── glossary.py
│   │   │       ├── simulations.py
│   │   │       ├── ai_chat.py
│   │   │       ├── ai_predict.py
│   │   │       └── billing.py
│   │   ├── services/              # Regras de negócio (portfolio_service, market_sync_service, etc.)
│   │   ├── ai/
│   │   │   ├── llm/                # LLMProvider interface + GroqProvider
│   │   │   └── ml/                 # Feature engineering, treino, inferência (Random Forest)
│   │   ├── integrations/          # Clients: brapi, bacen, tesouro, stripe, resend, google_oauth
│   │   └── jobs/                   # Scheduler de sincronização diária
│   ├── alembic/                    # Migrations
│   ├── tests/
│   ├── pyproject.toml
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   │   ├── landing/
│   │   │   ├── dashboard/
│   │   │   ├── portfolio/
│   │   │   ├── market/
│   │   │   ├── glossary/
│   │   │   ├── simulations/
│   │   │   ├── ai/
│   │   │   └── common/
│   │   ├── views/                  # Componentes de página, mapeados 1:1 nas rotas
│   │   ├── router/
│   │   ├── stores/                 # Pinia stores (auth, portfolio, ai, billing)
│   │   ├── services/                # Clients Axios por domínio
│   │   ├── i18n/                    # Arquivos de tradução pt-BR (estrutura pronta p/ novos idiomas)
│   │   ├── types/
│   │   └── main.ts
│   ├── public/
│   ├── vite.config.ts
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```
