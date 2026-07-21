# 8. Planos e Monetização

## 8.1 Estrutura de planos (recomendação)

Optado por manter **2 planos** no lançamento (mais simples de comunicar e de implementar controle de limites), com espaço para um plano "Pro" intermediário no futuro caso os dados de conversão indiquem essa necessidade.

| Recurso | Free | Premium |
|---|---|---|
| Carteira (nº de ativos ativos) | Até 10 posições | Ilimitado |
| Lançamentos de transações | Ilimitado | Ilimitado |
| Dashboard e comparação com benchmarks | Completo | Completo |
| Glossário de aprendizado | Completo | Completo |
| Simuladores | Completo | Completo |
| Chat de IA | 15 mensagens/mês | Ilimitado (fair-use) |
| Previsão de ML (fase 2) | Não disponível | Disponível (limite razoável/mês, ex: 30 previsões) |
| Suporte | Padrão (email) | Prioritário |
| Preço | R$ 0 | A definir (sugestão inicial de validação: R$ 19,90–29,90/mês) |

O glossário e os simuladores ficam completos mesmo no Free — são o principal motor de aquisição/SEO e ensino, e não fazem sentido como paywall dado o objetivo educacional do produto. O limite fica concentrado em carteira (uso intenso do produto) e IA (custo direto de API).

## 8.2 Integração de pagamento (Stripe)

- **Stripe Checkout** (hospedado) para simplificar PCI compliance — o backend nunca manipula dados de cartão diretamente.
- **Stripe Billing** para assinatura recorrente mensal, com suporte a upgrade/downgrade e cancelamento self-service via **Stripe Customer Portal**.
- **Webhooks** (`/billing/webhook`) processam eventos: `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`, `invoice.payment_failed` — cada um sincroniza o campo `status`/`plan` em `subscriptions`.
- Moeda: BRL. Métodos de pagamento: cartão de crédito (Pix/boleto via Stripe têm suporte limitado no Brasil — se validado como necessidade real dos usuários, avaliar Mercado Pago/Pagar.me como gateway adicional em fase futura, não bloqueante para o MVP).

## 8.3 Fair-use e prevenção de abuso

Mesmo no plano Premium "ilimitado", aplicar um teto técnico de fair-use (ex: 500 mensagens/mês) para proteger contra abuso/custo descontrolado de API do Groq, comunicado nos Termos de Uso.
