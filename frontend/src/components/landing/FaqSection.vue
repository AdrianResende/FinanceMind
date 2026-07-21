<script setup lang="ts">
const faqs = [
  {
    q: 'O FinanceMind dá recomendação de investimento?',
    a: 'Não. Todo o conteúdo, incluindo as respostas do chat de IA, é educativo e informativo. Não somos uma consultoria de investimentos registrada e nenhuma funcionalidade recomenda a compra ou venda de um ativo específico.',
  },
  {
    q: 'É gratuito?',
    a: 'Sim, existe um plano Free com acesso completo ao glossário, simuladores e dashboard, além de um limite mensal de mensagens no chat de IA. O plano Premium remove os limites.',
  },
  {
    q: 'Preciso conectar minha conta da corretora?',
    a: 'Não. Você lança suas compras e vendas manualmente. Não pedimos login ou dados de acesso de nenhuma corretora.',
  },
  {
    q: 'Meus dados estão seguros?',
    a: 'Sim. Senhas são armazenadas com hash (nunca em texto puro), a comunicação é criptografada e seus dados são tratados de acordo com a LGPD. Você pode excluir sua conta e seus dados a qualquer momento.',
  },
  {
    q: 'Quais ativos posso acompanhar?',
    a: 'No momento: Ações, FIIs, ETFs e Tesouro Direto. Renda fixa privada (CDB, LCI, LCA, Debêntures) está no roadmap.',
  },
]
</script>

<template>
  <v-container id="faq" class="py-12">
    <h2 class="text-h4 font-weight-bold text-center mb-10">Perguntas frequentes</h2>
    <v-responsive class="mx-auto" max-width="720">
      <v-expansion-panels variant="accordion">
        <v-expansion-panel v-for="faq in faqs" :key="faq.q" :title="faq.q" :text="faq.a" />
      </v-expansion-panels>
    </v-responsive>
  </v-container>
</template>
