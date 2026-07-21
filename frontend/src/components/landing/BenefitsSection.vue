<script setup lang="ts">
const benefits = [
  { icon: 'mdi-book-open-variant', text: 'Aprenda no seu ritmo, sem jargão desnecessário' },
  { icon: 'mdi-view-dashboard-outline', text: 'Toda sua carteira consolidada em um só lugar' },
  { icon: 'mdi-scale-balance', text: 'Compare sua rentabilidade com CDI, IPCA e IBOV' },
  { icon: 'mdi-chat-question-outline', text: 'Tire dúvidas a qualquer hora com a IA especializada' },
  { icon: 'mdi-calculator-variant-outline', text: 'Simule juros compostos e compare investimentos' },
  { icon: 'mdi-shield-check-outline', text: 'Sem recomendações disfarçadas — só conteúdo educativo' },
]
</script>

<template>
  <v-container id="beneficios" class="py-12" style="background: none">
    <h2 class="text-h4 font-weight-bold text-center mb-10">Por que usar o FinanceMind</h2>
    <v-row>
      <v-col v-for="benefit in benefits" :key="benefit.text" cols="12" sm="6" md="4">
        <div class="d-flex align-start ga-3">
          <v-icon :icon="benefit.icon" color="primary" />
          <span class="text-body-1">{{ benefit.text }}</span>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>
