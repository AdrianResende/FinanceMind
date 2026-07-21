<script setup lang="ts">
const pillars = [
  {
    icon: 'mdi-school-outline',
    title: 'Educação',
    text: 'Glossário claro sobre Ações, FIIs, ETFs, Tesouro Direto, CDB, dividendos, juros compostos e indicadores financeiros.',
  },
  {
    icon: 'mdi-chart-line',
    title: 'Acompanhamento',
    text: 'Sua carteira consolidada, com rentabilidade, alocação e comparação com CDI, IPCA e IBOV.',
  },
  {
    icon: 'mdi-robot-outline',
    title: 'Inteligência',
    text: 'Chat de IA especializado em investimentos para tirar dúvidas, sempre com avisos claros de que não é recomendação.',
  },
]
</script>

<template>
  <v-container id="sobre" class="py-12">
    <h2 class="text-h4 font-weight-bold text-center mb-2">Sobre o FinanceMind</h2>
    <p class="text-body-1 text-medium-emphasis text-center mx-auto mb-10" style="max-width: 640px">
      Não somos uma corretora, nem um app de controle de gastos. Somos uma plataforma para você
      entender o que está comprando e acompanhar sua evolução como investidor.
    </p>
    <v-row>
      <v-col v-for="pillar in pillars" :key="pillar.title" cols="12" md="4">
        <v-card class="pa-6 h-100" variant="outlined">
          <v-icon :icon="pillar.icon" size="40" color="primary" class="mb-3" />
          <h3 class="text-h6 font-weight-bold mb-2">{{ pillar.title }}</h3>
          <p class="text-body-2 text-medium-emphasis">{{ pillar.text }}</p>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
