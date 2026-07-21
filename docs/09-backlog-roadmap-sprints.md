# 9. Backlog, Roadmap e Sprints

## 9.1 Épicos

- **E0 — Fundação técnica**: setup de repositório, Docker Compose, CI básico, estrutura de pastas.
- **E1 — Autenticação e Contas**: cadastro, login, Google OAuth, gestão de sessão.
- **E2 — Landing Page**: todas as seções públicas de marketing.
- **E3 — Carteira**: cadastro de ativos suportados, lançamento de transações, cálculo de posição/rentabilidade.
- **E4 — Mercado**: sincronização de cotações/benchmarks, tela de detalhe de ativo.
- **E5 — Dashboard**: agregações e gráficos (rentabilidade, alocação, dividendos, benchmarks, top movers).
- **E6 — Aprendizado (Glossário)**: conteúdo e navegação do dicionário de termos.
- **E7 — Simulações**: juros compostos e comparação entre ativos.
- **E8 — IA Chat**: integração Groq/LangChain, histórico, rate limit.
- **E9 — Planos e Billing**: Stripe, limites por plano, portal do cliente.
- **E10 — Legal e Compliance**: disclaimers, minutas de Termos/Privacidade, LGPD.
- **E11 — IA Previsão (ML)**: pipeline Random Forest (fase 2).
- **E12 — Renda fixa privada**: CDB/LCI/LCA/Debêntures/Fundos (fase 2).

## 9.2 Backlog (User Stories por épico, prioridade dentro do MVP)

### E0 — Fundação técnica
- Como dev, quero um `docker-compose.yml` com backend, frontend, Postgres e Redis, para rodar o projeto localmente com um comando.
- Como dev, quero estrutura de pastas definida em backend e frontend, para manter consistência desde o primeiro commit.
- Como dev, quero Alembic configurado, para versionar o schema do banco desde a primeira migration.

### E1 — Autenticação
- Como visitante, quero me cadastrar com email/senha, para criar minha conta.
- Como visitante, quero entrar com Google, para não precisar criar outra senha.
- Como usuário, quero recuperar minha senha por email, para não perder acesso à conta.
- Como usuário, quero que minha sessão seja renovada automaticamente, para não ser deslogado a cada 15 minutos.

### E2 — Landing Page
- Como visitante, quero entender o que o produto faz na primeira dobra (Hero), para decidir se quero me cadastrar.
- Como visitante, quero ver os planos e preços, para avaliar antes de assinar.
- Como visitante, quero ver FAQ e depoimentos, para reduzir minha incerteza antes de me cadastrar.

### E3 — Carteira
- Como usuário, quero lançar uma compra de ação/FII/ETF/Tesouro Direto, para começar a acompanhar minha carteira.
- Como usuário, quero editar/excluir um lançamento, para corrigir erros de digitação.
- Como usuário, quero ver minha posição consolidada por ativo, para saber quanto tenho investido em cada um.

### E4 — Mercado
- Como usuário, quero buscar um ativo por ticker/nome, para lançar uma transação rapidamente.
- Como usuário, quero ver o histórico de preços de um ativo, para entender sua evolução.
- Como sistema, quero sincronizar cotações diariamente, para manter os dados atualizados sem depender de chamada em tempo real a cada acesso.

### E5 — Dashboard
- Como usuário, quero ver meu patrimônio total e rentabilidade, para acompanhar minha evolução como investidor.
- Como usuário, quero comparar minha carteira com CDI/IPCA/IBOV, para saber se estou performando bem.
- Como usuário, quero ver quais ativos mais subiram/caíram, para entender o que impactou meu resultado.

### E6 — Aprendizado
- Como usuário iniciante, quero buscar o significado de "FII" ou "Tesouro Selic", para entender o que estou comprando.
- Como usuário, quero navegar por categoria (renda fixa, renda variável, etc.), para explorar o conteúdo de forma organizada.

### E7 — Simulações
- Como usuário, quero simular juros compostos com meus próprios valores, para entender o poder do longo prazo.
- Como usuário, quero comparar CDB vs Tesouro vs uma ação no mesmo período, para entender diferenças de risco/retorno.

### E8 — IA Chat
- Como usuário, quero perguntar "o que é Tesouro IPCA+" no chat, para tirar dúvidas sem sair da plataforma.
- Como usuário, quero ver um aviso claro de que a IA não dá recomendação de investimento, para entender os limites da ferramenta.
- Como usuário Free, quero saber quantas mensagens de IA ainda tenho no mês, para gerenciar meu uso.

### E9 — Planos e Billing
- Como usuário Free, quero fazer upgrade para Premium, para ter acesso ilimitado à IA e à carteira.
- Como usuário Premium, quero gerenciar/cancelar minha assinatura, para ter controle sobre minha cobrança.

### E10 — Legal e Compliance
- Como responsável pelo produto, quero uma minuta de Termos de Uso e Política de Privacidade, para levar à revisão jurídica antes do lançamento público.
- Como usuário, quero ver disclaimers claros em toda saída de IA, para entender que não é aconselhamento financeiro.

### E11 — IA Previsão (fase 2)
- Como usuário Premium, quero gerar uma previsão de tendência para um ativo elegível, para ter mais um dado de apoio à minha análise.

### E12 — Renda fixa privada (fase 2)
- Como usuário, quero lançar um CDB/LCI/LCA na carteira, para consolidar 100% dos meus investimentos na plataforma.

## 9.3 Milestones

| Milestone | Conteúdo | Épicos |
|---|---|---|
| **M0 — Fundação** | Repositório, Docker Compose, CI básico, estrutura de pastas | E0 |
| **M1 — Acesso** | Landing page + autenticação completa (email/senha + Google) | E1, E2 |
| **M2 — Carteira core** | Cadastro de ativos, lançamento de transações, posição consolidada | E3, E4 (parcial) |
| **M3 — Dashboard** | Todos os gráficos e comparações do dashboard | E5 |
| **M4 — Aprendizado e Simulações** | Glossário completo + simuladores | E6, E7 |
| **M5 — IA Chat** | Chat funcional com Groq, histórico, rate limit | E8 |
| **M6 — Monetização** | Planos, Stripe, limites por plano | E9 |
| **M7 — Compliance e Lançamento Beta** | Disclaimers, minutas legais, hardening de segurança, deploy real | E10 |
| **M8 — IA Previsão (fase 2)** | Pipeline de ML completo | E11 |
| **M9 — Expansão de ativos (fase 2)** | Renda fixa privada | E12 |

## 9.4 Sprints sugeridos (ciclos de 2 semanas, ritmo referencial — sem data fixa)

| Sprint | Foco | Entrega |
|---|---|---|
| Sprint 1 | M0 completo + início M1 | Ambiente rodando, telas de login/cadastro funcionais (sem Google ainda) |
| Sprint 2 | M1 completo | Google OAuth, recuperação de senha, landing page publicada |
| Sprint 3 | M2 (parte 1) | Catálogo de ativos + sincronização brapi.dev/BACEN/Tesouro Transparente |
| Sprint 4 | M2 (parte 2) | CRUD de transações + cálculo de posição/rentabilidade (custo médio) |
| Sprint 5 | M3 | Dashboard completo com todos os gráficos e benchmarks |
| Sprint 6 | M4 | Glossário + simuladores |
| Sprint 7 | M5 | Chat de IA (Groq) integrado, com histórico e rate limit |
| Sprint 8 | M6 | Stripe, planos Free/Premium, limites aplicados |
| Sprint 9 | M7 | Disclaimers finais, minutas legais entregues para revisão jurídica, revisão de segurança, deploy em produção (Vercel/Railway/Supabase) |
| Sprint 10+ | M8 e M9 | Início da fase 2: modelo de ML e renda fixa privada |

## 9.5 Definition of Done (referência para todas as sprints)

- Código com testes unitários para regras de negócio críticas (cálculo de rentabilidade, autenticação, rate limit de IA).
- Sem segredos hardcoded (tudo via variável de ambiente).
- Endpoint documentado (OpenAPI gerado automaticamente pelo FastAPI, revisado).
- Disclaimers de IA presentes onde aplicável.
- Testado manualmente no fluxo principal antes de considerar a story concluída.
