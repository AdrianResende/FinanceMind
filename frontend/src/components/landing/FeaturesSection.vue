<script setup lang="ts">
const features = [
  { icon: 'mdi-view-dashboard-outline', title: 'Home', text: 'Painel com patrimônio, rentabilidade e evolução da carteira.' },
  { icon: 'mdi-briefcase-outline', title: 'Carteira', text: 'Lance suas compras e vendas e acompanhe sua posição consolidada.' },
  { icon: 'mdi-chart-areaspline', title: 'Mercado', text: 'Cotações e histórico de Ações, FIIs, ETFs e Tesouro Direto.' },
  { icon: 'mdi-book-education-outline', title: 'Aprendizado', text: 'Glossário completo dos principais termos do mercado financeiro.' },
  { icon: 'mdi-calculator-variant-outline', title: 'Simulações', text: 'Juros compostos e comparação entre diferentes investimentos.' },
  { icon: 'mdi-robot-outline', title: 'IA', text: 'Assistente especializado para tirar dúvidas sobre investimentos.' },
]
</script>

<template>
  <v-container id="recursos" class="py-12">
    <h2 class="text-h4 font-weight-bold text-center mb-10">Recursos</h2>
    <v-row>
      <v-col v-for="feature in features" :key="feature.title" cols="12" sm="6" md="4">
        <v-card class="pa-6 h-100" variant="flat" color="surface-variant" rounded="lg">
          <v-icon :icon="feature.icon" size="32" color="primary" class="mb-3" />
          <h3 class="text-subtitle-1 font-weight-bold mb-1">{{ feature.title }}</h3>
          <p class="text-body-2 text-medium-emphasis">{{ feature.text }}</p>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
