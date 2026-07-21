# 4. Especificação de API (REST)

Prefixo base: `/api/v1`. Autenticação via `Authorization: Bearer <access_token>` exceto onde indicado como público. Respostas de erro seguem formato padrão `{ "error": { "code": "...", "message": "..." } }`.

## 4.1 Auth (`/auth`)

| Método | Rota | Descrição | Auth |
|---|---|---|---|
| POST | `/auth/register` | Cria conta (email/senha) | Público |
| POST | `/auth/login` | Login email/senha, retorna tokens | Público |
| POST | `/auth/refresh` | Renova access_token via refresh_token | Cookie |
| POST | `/auth/logout` | Invalida refresh_token | Cookie |
| GET | `/auth/google/login` | Inicia fluxo OAuth Google | Público |
| GET | `/auth/google/callback` | Callback OAuth Google | Público |
| POST | `/auth/verify-email` | Confirma email via token enviado | Público |
| POST | `/auth/forgot-password` | Envia email de reset | Público |
| POST | `/auth/reset-password` | Define nova senha via token | Público |

## 4.2 Usuário e Perfil (`/users`)

| Método | Rota | Descrição |
|---|---|---|
| GET | `/users/me` | Dados do usuário logado + plano atual |
| PATCH | `/users/me` | Atualiza nome/preferências |
| DELETE | `/users/me` | Exclusão de conta (LGPD) |

## 4.3 Carteira (`/portfolio`)

| Método | Rota | Descrição |
|---|---|---|
| GET | `/portfolio` | Retorna carteira consolidada: posições atuais, valor investido, valor atual, rentabilidade |
| GET | `/portfolio/allocation` | Alocação por classe de ativo (para gráfico de pizza/donut) |
| GET | `/portfolio/dividends` | Histórico e projeção de dividendos recebidos |
| GET | `/portfolio/performance` | Série histórica de evolução patrimonial |
| GET | `/portfolio/benchmarks` | Comparação da carteira vs CDI/IPCA/IBOV no período |
| GET | `/portfolio/top-movers` | Ativos que mais subiram/caíram na carteira |
| GET | `/transactions` | Lista transações (paginada, filtrável por ativo/data) |
| POST | `/transactions` | Cria transação (compra/venda) |
| PATCH | `/transactions/{id}` | Edita transação |
| DELETE | `/transactions/{id}` | Remove transação |

## 4.4 Mercado (`/market`)

| Método | Rota | Descrição |
|---|---|---|
| GET | `/market/assets` | Busca/lista ativos suportados (autocomplete ao lançar transação) |
| GET | `/market/assets/{ticker}` | Detalhe de um ativo + cotação atual + indicadores |
| GET | `/market/assets/{ticker}/history` | Série histórica de preços (para gráfico) |
| GET | `/market/benchmarks/{code}` | Série histórica de um benchmark (CDI/IPCA/IBOV) |

## 4.5 Aprendizado / Glossário (`/glossary`)

| Método | Rota | Descrição |
|---|---|---|
| GET | `/glossary/categories` | Lista categorias |
| GET | `/glossary/terms` | Lista termos (filtrável por categoria, busca por texto) |
| GET | `/glossary/terms/{slug}` | Detalhe de um termo |

## 4.6 Simulações (`/simulations`)

| Método | Rota | Descrição |
|---|---|---|
| POST | `/simulations/compound-interest` | Calcula evolução de juros compostos (aporte inicial, mensal, taxa, prazo) |
| POST | `/simulations/compare-assets` | Compara rentabilidade histórica simulada entre 2+ ativos/indexadores |

## 4.7 IA — Chat (`/ai/chat`)

| Método | Rota | Descrição |
|---|---|---|
| GET | `/ai/chat/conversations` | Lista conversas do usuário |
| POST | `/ai/chat/conversations` | Cria nova conversa |
| GET | `/ai/chat/conversations/{id}` | Histórico de mensagens |
| POST | `/ai/chat/conversations/{id}/messages` | Envia mensagem, retorna resposta da IA (aplica rate limit do plano) |
| DELETE | `/ai/chat/conversations/{id}` | Remove conversa |

## 4.8 IA — Previsão ML (`/ai/predict`) — Fase 2

| Método | Rota | Descrição |
|---|---|---|
| GET | `/ai/predict/eligible-assets` | Lista ativos elegíveis para previsão (curados) |
| POST | `/ai/predict/{ticker}` | Gera previsão sob demanda (feature Premium) |
| GET | `/ai/predict/history` | Histórico de previsões geradas pelo usuário |

## 4.9 Billing (`/billing`)

| Método | Rota | Descrição |
|---|---|---|
| GET | `/billing/plans` | Lista planos disponíveis e limites |
| POST | `/billing/checkout-session` | Cria sessão de checkout Stripe para upgrade |
| POST | `/billing/portal-session` | Cria sessão do portal do cliente Stripe (gerenciar assinatura) |
| POST | `/billing/webhook` | Endpoint de webhook do Stripe (sem auth de usuário, valida assinatura Stripe) |

## 4.10 Convenções gerais

- Paginação: `?page=1&page_size=20`, resposta com `{ items, total, page, page_size }`.
- Datas em ISO 8601, valores monetários em `numeric` com 2-8 casas decimais dependendo do ativo (cotas de FII/ETF podem ter mais casas).
- Rate limiting por plano aplicado via middleware, com header de resposta `X-RateLimit-Remaining`.
- Toda resposta de `/ai/chat` e `/ai/predict` inclui campo `disclaimer` fixo, nunca omitido pelo frontend.
