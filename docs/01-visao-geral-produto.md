# 1. Visão Geral do Produto

## 1.1 Problema

Investidores iniciantes e intermediários no Brasil têm acesso a corretoras e apps de acompanhamento de carteira, mas raramente encontram, no mesmo lugar: educação prática sobre os instrumentos que estão comprando, acompanhamento real da própria carteira, e um ponto de dúvidas confiável para perguntas do dia a dia sobre investimentos. Ferramentas de controle financeiro pessoal (tipo Mobills, Organizze) focam em despesas, não em entender e evoluir como investidor.

## 1.2 Proposta de valor

**FinanceMind** é uma plataforma que une três pilares:

1. **Educação** — glossário claro sobre Ações, FIIs, ETFs, Tesouro Direto, CDB, LCI, LCA, Debêntures, Fundos, dividendos, juros compostos e indicadores financeiros.
2. **Acompanhamento** — carteira de investimentos com rentabilidade, alocação, dividendos e comparação com benchmarks (CDI, IPCA, IBOV).
3. **Inteligência** — um assistente de IA especializado em investimentos para tirar dúvidas, e um modelo de Machine Learning que apresenta probabilidades de tendência de curto prazo (sempre com disclaimers claros de que não é recomendação de investimento).

## 1.3 Público-alvo

- **Persona 1 — Iniciante curioso**: nunca investiu ou começou há pouco tempo, não entende a diferença entre CDB e Tesouro Direto, quer aprender no próprio ritmo sem jargão.
- **Persona 2 — Intermediário organizado**: já investe em ações/FIIs/Tesouro, usa planilha ou app da corretora, quer consolidar tudo em um lugar com visão de rentabilidade e comparação com benchmarks.
- **Persona 3 — Curioso por tecnologia/IA**: quer usar ferramentas de IA para tirar dúvidas rápidas e ver previsões de mercado como um complemento (não substituto) de sua própria análise.

## 1.4 Fora de escopo (explícito)

- **Não é** um controle de despesas pessoais (não há orçamento, categorização de gastos, contas correntes).
- **Não é** uma corretora — não executa ordens de compra/venda reais, não custodia ativos.
- **Não é** consultoria de investimento registrada na CVM — toda saída de IA é educativa/informativa, nunca uma recomendação personalizada.
- Integrações automáticas com corretoras (Open Finance) **não** fazem parte do MVP.

## 1.5 Escopo do MVP (Fase 1)

**Incluído:**
- Landing page completa (Hero, Sobre, Benefícios, Recursos, Planos, FAQ, Depoimentos, Contato, Login, Cadastro)
- Autenticação (email/senha + Google OAuth), planos Free/Premium (estrutura pronta, cobrança via Stripe)
- Dashboard com carteira consolidada, rentabilidade, alocação, dividendos, comparação com CDI/IPCA/IBOV, evolução patrimonial, maiores altas/baixas
- Carteira: lançamento manual de transações (compra/venda) para Ações, FIIs, ETFs e Tesouro Direto
- Mercado: cotações e indicadores dos ativos suportados
- Aprendizado: glossário de termos financeiros
- Simulações: juros compostos + comparação entre ativos
- IA — Chat especializado em investimentos (Groq/Llama)
- Perfil e Configurações

**Fase 2 (pós-MVP, já mapeado no roadmap):**
- Modelo de ML (Random Forest) de previsão de tendência de curto prazo
- Renda fixa privada (CDB, LCI, LCA, Debêntures, Fundos)
- Trilhas de aprendizado com quiz (evolução do glossário)
- TWR (Time-Weighted Return) como método de cálculo de rentabilidade
- Importação de CSV/nota de corretagem
- Plano "Pro" intermediário, caso a métrica de conversão indique necessidade

## 1.6 Idioma e localização

Interface em português do Brasil (pt-BR) desde o início, mas com todos os textos organizados via arquivos de i18n (vue-i18n) para permitir expansão futura para outros idiomas sem refatoração estrutural.

## 1.7 Nome e identidade

Nome de trabalho e definitivo: **FinanceMind**. Domínio ainda não definido — não é bloqueante para o desenvolvimento local.
