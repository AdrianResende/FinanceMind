<script setup lang="ts">
const pillars = [
  {
    icon: 'school-outline',
    title: 'Educação',
    text: 'Glossário claro sobre Ações, FIIs, ETFs, Tesouro Direto, CDB, dividendos, juros compostos e indicadores financeiros.',
  },
  {
    icon: 'chart-line',
    title: 'Acompanhamento',
    text: 'Sua carteira consolidada, com rentabilidade, alocação e comparação com CDI, IPCA e IBOV.',
  },
  {
    icon: 'robot-outline',
    title: 'Inteligência',
    text: 'Chat de IA especializado em investimentos para tirar dúvidas, sempre com avisos claros de que não é recomendação.',
  },
]
</script>

<template>
  <section id="sobre" class="page-shell section-py">
    <h2 class="text-section-title text-center">Sobre o FinanceMind</h2>
    <p class="text-lead text-center section-intro">
      Não somos uma corretora, nem um app de controle de gastos. Somos uma plataforma para você
      entender o que está comprando e acompanhar sua evolução como investidor.
    </p>

    <n-grid :x-gap="24" :y-gap="24" cols="1 s:3" responsive="screen">
      <n-grid-item v-for="pillar in pillars" :key="pillar.title">
        <n-card bordered hoverable content-style="padding: 24px" class="glass-card h-100">
          <div class="icon-tile mb-4">
            <MdiIcon :name="pillar.icon" :size="24" />
          </div>
          <h3 class="text-title mb-2">{{ pillar.title }}</h3>
          <p class="text-body">{{ pillar.text }}</p>
        </n-card>
      </n-grid-item>
    </n-grid>
  </section>
</template>

<style scoped>
.section-intro {
  max-width: 640px;
  margin-inline: auto;
  margin-block: var(--space-3) var(--space-8);
}
</style>
