# FinanceMind — Documentação do Projeto

Índice da documentação completa, construída a partir do alinhamento de escopo feito antes do início do desenvolvimento.

1. [Visão Geral do Produto](./01-visao-geral-produto.md)
2. [Arquitetura Técnica](./02-arquitetura-tecnica.md)
3. [Modelo de Dados](./03-modelo-dados.md)
4. [Especificação de API](./04-especificacao-api.md)
5. [Telas, Componentes e Fluxos](./05-telas-componentes-fluxos.md)
6. [IA: Chat especializado (LLM) e Previsão (ML)](./06-ia-llm-ml.md)
7. [Segurança, Compliance e Legal](./07-seguranca-compliance-legal.md)
8. [Planos e Monetização](./08-planos-monetizacao.md)
9. [Backlog, Roadmap e Sprints](./09-backlog-roadmap-sprints.md)

## Decisões fechadas (referência rápida)

| Tema | Decisão |
|---|---|
| Nome do produto | FinanceMind |
| Escopo do MVP | Lean: Aprendizado (glossário) + Carteira manual + Dashboard. IA chat entra logo em seguida; ML preditivo é fase posterior |
| Ativos suportados no MVP | Renda Variável (Ações, FIIs, ETFs) + Tesouro Direto. Renda fixa privada (CDB/LCI/LCA/Debêntures/Fundos) fica para fase 2 |
| Fonte de dados de mercado | brapi.dev (B3) + BACEN SGS (CDI/IPCA/Selic) + Tesouro Transparente (Tesouro Direto) |
| Entrada da carteira | Lançamento manual de transações (compra/venda) |
| Cálculo de rentabilidade | Método simples (custo médio) no MVP; migrar para TWR é melhoria futura documentada |
| Módulo de Aprendizado | Glossário/dicionário de termos financeiros (sem trilhas/quiz no MVP) |
| Simulador | Juros compostos + comparação entre ativos (ex: CDB vs Tesouro vs Ação) |
| LLM do chat | Groq (Llama 3.x), com camada de abstração para trocar por OpenAI/Claude/Gemini depois |
| ML preditivo | Random Forest, sob demanda, lista curta de ativos líquidos, histórico diário de 1-2 anos |
| Autenticação | Email/senha (JWT access+refresh) + Login com Google (OAuth2) |
| Monetização | Freemium — 2 planos (Free e Premium) |
| Pagamento | Stripe |
| Email transacional | Resend |
| Banco (dev) | PostgreSQL via Docker Compose local; Supabase Postgres em produção |
| Deploy (futuro) | Frontend: Vercel · Backend: Railway/Render · DB: Supabase |
| Idioma | Português (pt-BR), já estruturado com i18n para expansão futura |
| Compliance | Disclaimers obrigatórios na UI + minuta de Termos de Uso/Privacidade para revisão jurídica antes do lançamento público (não substitui advogado) |
| Equipe | Solo (usuário + Claude Code) |
| Testes | Testes unitários essenciais no backend (regras de negócio críticas) |
| Prazo | Sem prazo fixo — ritmo orientado por milestones, não datas |
