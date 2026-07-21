# 6. IA — Chat Especializado (LLM) e Previsão (ML)

## 6.1 Chat de IA especializado em investimentos

### Provedor
Groq (free tier), modelo recomendado: `llama-3.3-70b-versatile` (bom equilíbrio entre qualidade em português e velocidade/custo zero). Acesso via LangChain, usando a interface `LLMProvider` descrita em [02-arquitetura-tecnica.md](./02-arquitetura-tecnica.md#28-camada-de-abstração-de-llm-importante-para-troca-futura) para permitir trocar por OpenAI/Claude/Gemini sem reescrever a lógica de chat.

### Escopo de resposta
O assistente deve responder apenas sobre: investimentos, renda fixa, renda variável, indicadores financeiros, impostos sobre investimentos, dividendos e estratégias gerais de alocação. Perguntas fora desse escopo (ex: assuntos não financeiros) devem ser educadamente recusadas, redirecionando ao propósito do produto.

### Guardrails obrigatórios (system prompt)
1. Nunca recomendar a compra/venda de um ativo específico como se fosse aconselhamento personalizado — sempre enquadrar como educativo/informativo.
2. Toda resposta sobre ativos ou estratégias deve reforçar que rentabilidade passada não garante rentabilidade futura.
3. Disclaimer fixo exibido na UI abaixo de cada resposta (não depende do texto gerado pelo modelo, é aplicado pelo backend): *"Este conteúdo é educativo e não constitui recomendação de investimento. Consulte um profissional certificado antes de tomar decisões financeiras."*
4. Sanitização de prompt injection: mensagens do usuário nunca sobrescrevem o system prompt; inputs são tratados como dados, não como instruções ao sistema.

### Persistência e limites
Conversas e mensagens persistidas em `ai_conversations`/`ai_messages`. Rate limit por plano (ex: Free = 10 mensagens/mês, Premium = alto limite ou ilimitado com fair-use) aplicado por middleware antes de chamar o provider, para não gastar quota de API em requisições que serão bloqueadas.

## 6.2 Modelo de Previsão (Machine Learning) — Fase 2

### Objetivo e limites claros
Estimar a **probabilidade direcional** (alta/baixa) de um ativo em um horizonte curto (ex: próximos 5 dias úteis), **não** um preço-alvo. É uma ferramenta educativa de apoio, não um sinal de trading.

### Escopo de ativos (MVP da feature)
Lista curta e curada de ativos líquidos da B3 (ex: 20-30 tickers do IBOV + FIIs mais negociados), sob demanda (o usuário clica em "gerar previsão"), não automático para toda a carteira — decisão já validada para controlar custo computacional e evitar previsões de baixa qualidade em ativos ilíquidos.

### Pipeline
1. **Dados**: histórico diário (`asset_price_history`) dos últimos 1-2 anos.
2. **Feature engineering**: retornos diários/semanais, médias móveis (7/21/50 dias), RSI, volatilidade histórica (desvio-padrão dos retornos), volume relativo.
3. **Target**: binário — se o retorno acumulado nos próximos N dias úteis (ex: 5) é positivo ou negativo.
4. **Modelo**: `RandomForestClassifier` (scikit-learn), com validação temporal (walk-forward, nunca `train_test_split` aleatório — dados financeiros são sequenciais).
5. **Saída**: probabilidade da classe "alta" (`predict_proba`), e uma métrica de confiança derivada da concordância entre as árvores da floresta.
6. **Persistência do modelo**: `joblib`, versão do modelo (`model_version`) registrada em cada `ml_predictions` para rastreabilidade.
7. **Retreino**: periódico (ex: mensal), não em tempo real — mudanças de mercado são incorporadas gradualmente.

### Disclaimers obrigatórios na resposta (aplicados pelo backend, sempre visíveis)
- "Esta é uma estimativa estatística baseada em dados históricos, não uma garantia ou recomendação de investimento."
- "Eventos inesperados (notícias, crises, mudanças macroeconômicas) podem invalidar completamente esta previsão."
- Exibir sempre `probabilidade` e `confiança` lado a lado — nunca um número isolado sem contexto de incerteza.

### Por que "Fase 2"
Já decidido que o MVP entrega carteira + aprendizado + chat de IA primeiro; o modelo de ML entra na sequência (ver [09-backlog-roadmap-sprints.md](./09-backlog-roadmap-sprints.md)) para não atrasar a validação do core do produto com uma feature de maior complexidade técnica e de governança de dados.
