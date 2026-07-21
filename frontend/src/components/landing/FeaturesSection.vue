<script setup lang="ts">
const features = [
  { icon: 'view-dashboard-outline', title: 'Home', text: 'Painel com patrimônio, rentabilidade e evolução da carteira.' },
  { icon: 'briefcase-outline', title: 'Carteira', text: 'Lance suas compras e vendas e acompanhe sua posição consolidada.' },
  { icon: 'chart-areaspline', title: 'Mercado', text: 'Cotações e histórico de Ações, FIIs, ETFs e Tesouro Direto.' },
  { icon: 'book-education-outline', title: 'Aprendizado', text: 'Glossário completo dos principais termos do mercado financeiro.' },
  { icon: 'calculator-variant-outline', title: 'Simulações', text: 'Juros compostos e comparação entre diferentes investimentos.' },
  { icon: 'robot-outline', title: 'IA', text: 'Assistente especializado para tirar dúvidas sobre investimentos.' },
]
</script>

<template>
  <section id="recursos" class="page-shell section-py">
    <h2 class="text-section-title text-center mb-8">Recursos</h2>

    <n-grid :x-gap="24" :y-gap="24" cols="1 s:2 l:3" responsive="screen">
      <n-grid-item v-for="feature in features" :key="feature.title">
        <n-card bordered hoverable content-style="padding: 24px" class="glass-card h-100">
          <div class="icon-tile mb-4">
            <MdiIcon :name="feature.icon" :size="24" />
          </div>
          <h3 class="text-title mb-2">{{ feature.title }}</h3>
          <p class="text-body">{{ feature.text }}</p>
        </n-card>
      </n-grid-item>
    </n-grid>
  </section>
</template>
