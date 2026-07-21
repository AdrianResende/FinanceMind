# 7. Segurança, Compliance e Legal

## 7.1 Segurança técnica

| Área | Prática |
|---|---|
| Senhas | Hash com Argon2id (via `passlib`), nunca armazenadas em texto plano |
| Tokens | JWT assinado (RS256 recomendado), access token curto (15 min), refresh token em cookie `httpOnly` + `Secure` + `SameSite=Lax`, rotação de refresh token a cada uso |
| Transporte | HTTPS obrigatório em produção (Vercel/Railway já fornecem TLS por padrão) |
| CORS | Whitelist explícita de origens (frontend), nunca `*` em produção |
| Validação de entrada | Pydantic v2 em todos os endpoints; nunca confiar em dados do cliente sem validação de tipo/formato |
| Segredos | `.env` local (nunca commitado, incluir em `.gitignore` desde o commit inicial); variáveis de ambiente no provedor em produção; chaves de API (Groq, Stripe, Resend) nunca expostas ao frontend |
| Rate limiting | Middleware de rate limit por usuário/IP em endpoints sensíveis (login, IA, previsão) para mitigar brute-force e abuso de custo de API |
| Webhook Stripe | Validação obrigatória da assinatura (`Stripe-Signature`) antes de processar qualquer evento |
| Logs | Nunca logar senha, token completo ou dados de cartão (Stripe já cuida disso via tokenização — o backend nunca deve tocar em dados de cartão) |
| Dependências | Atualização periódica e checagem de vulnerabilidades (ex: `pip-audit`, `npm audit`) |

## 7.2 LGPD (Lei Geral de Proteção de Dados)

Como o produto trata dados financeiros pessoais (carteira de investimentos, transações), aplica-se a LGPD:

- Base legal: consentimento no cadastro + execução de contrato (prestação do serviço).
- Direitos do titular a implementar: exportação de dados (fase 2), exclusão de conta (`DELETE /users/me` já especificado), correção de dados.
- Minimização: coletar apenas o necessário (email, nome, dados de carteira informados pelo próprio usuário) — nunca solicitar CPF, dados bancários ou credenciais de corretora no MVP.
- Retenção: dados mantidos enquanto a conta existir; política de retenção pós-exclusão a definir com o time jurídico.

## 7.3 Disclaimers obrigatórios de produto (não-negociáveis na UI)

1. **Chat de IA**: disclaimer fixo em toda resposta — conteúdo educativo, não é recomendação de investimento.
2. **Previsão de ML**: disclaimer duplo — não é garantia, e eventos inesperados podem invalidar a previsão (ver [06-ia-llm-ml.md](./06-ia-llm-ml.md)).
3. **Rodapé geral do produto**: nota de que a plataforma é educativa/informativa e não substitui um profissional certificado (CFP, agente autônomo de investimento) nem constitui análise da CVM.

## 7.4 Termos de Uso e Política de Privacidade — minuta para revisão jurídica

**Importante**: como deixado claro durante o alinhamento de escopo, esta documentação **não substitui revisão por um advogado**. O que será entregue é uma **minuta estruturada** cobrindo os pontos abaixo, para ser revisada e ajustada por um profissional antes do lançamento público — isso é um item obrigatório do backlog (marcado como bloqueante de lançamento, não do desenvolvimento).

**Termos de Uso — tópicos a cobrir na minuta:**
- Natureza do serviço (educativo/informativo, não é corretora nem consultoria registrada)
- Isenção de responsabilidade sobre decisões de investimento tomadas com base no conteúdo/IA da plataforma
- Regras de uso aceitável (proibição de abuso do chat de IA, engenharia reversa, etc.)
- Condições de assinatura, cancelamento e reembolso (alinhado às regras do Stripe/Código de Defesa do Consumidor)
- Propriedade intelectual do conteúdo do glossário e das análises geradas

**Política de Privacidade — tópicos a cobrir na minuta:**
- Quais dados são coletados (cadastro, carteira, uso do chat) e finalidade de cada um
- Compartilhamento com terceiros (Stripe para pagamento, Groq para processamento das mensagens do chat, Resend para email) — deixar explícito que mensagens do chat podem ser processadas por provedor de IA terceiro
- Direitos do titular sob a LGPD e como exercê-los
- Prazo de retenção e processo de exclusão de dados

## 7.5 Regulatório (CVM)

A plataforma **não é** registrada como consultora de valores mobiliários. Por isso:
- Nenhuma funcionalidade deve gerar recomendação personalizada e individualizada de compra/venda vinculada ao perfil do usuário.
- O texto de toda comunicação (marketing, chat, previsão de ML) deve manter linguagem educativa/estatística, evitando termos como "recomendamos" ou "você deveria comprar".
- Caso o roadmap evolua para consultoria personalizada no futuro, será necessária análise jurídica específica sobre registro na CVM antes de lançar tal feature — está fora do escopo atual.
