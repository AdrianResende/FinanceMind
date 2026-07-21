<script setup lang="ts">
const benefits = [
  { icon: 'book-open-variant', text: 'Aprenda no seu ritmo, sem jargão desnecessário' },
  { icon: 'view-dashboard-outline', text: 'Toda sua carteira consolidada em um só lugar' },
  { icon: 'scale-balance', text: 'Compare sua rentabilidade com CDI, IPCA e IBOV' },
  { icon: 'chat-question-outline', text: 'Tire dúvidas a qualquer hora com a IA especializada' },
  { icon: 'calculator-variant-outline', text: 'Simule juros compostos e compare investimentos' },
  { icon: 'shield-check-outline', text: 'Sem recomendações disfarçadas — só conteúdo educativo' },
]
</script>

<template>
  <section id="beneficios" class="page-shell section-py">
    <h2 class="text-section-title text-center mb-8">Por que usar o FinanceMind</h2>

    <n-grid :x-gap="24" :y-gap="24" cols="1 s:2 l:3" responsive="screen">
      <n-grid-item v-for="benefit in benefits" :key="benefit.text">
        <n-card bordered hoverable content-style="padding: 24px" class="glass-card h-100">
          <div class="benefit-row">
            <div class="icon-tile icon-tile--sm">
              <MdiIcon :name="benefit.icon" :size="20" />
            </div>
            <span class="text-body">{{ benefit.text }}</span>
          </div>
        </n-card>
      </n-grid-item>
    </n-grid>
  </section>
</template>

<style scoped>
.benefit-row {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}
</style>
