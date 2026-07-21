<script setup lang="ts">
// Placeholder — substituir por depoimentos reais de usuários beta antes do lançamento público.
const testimonials = [
  {
    name: 'Usuário Beta 1',
    text: 'Depoimento de exemplo — em breve substituído por feedback real de usuários do beta.',
  },
  {
    name: 'Usuário Beta 2',
    text: 'Depoimento de exemplo — em breve substituído por feedback real de usuários do beta.',
  },
  {
    name: 'Usuário Beta 3',
    text: 'Depoimento de exemplo — em breve substituído por feedback real de usuários do beta.',
  },
]
</script>

<template>
  <section id="depoimentos" class="page-shell section-py">
    <h2 class="text-section-title text-center mb-2">O que dizem sobre o FinanceMind</h2>
    <p class="text-muted text-center mb-8">
      Depoimentos ilustrativos — serão substituídos por relatos reais de usuários assim que o
      programa beta tiver feedback suficiente.
    </p>

    <n-grid :x-gap="24" :y-gap="24" cols="1 s:3" responsive="screen">
      <n-grid-item v-for="t in testimonials" :key="t.name">
        <n-card bordered hoverable content-style="padding: 24px" class="glass-card h-100">
          <MdiIcon name="format-quote-open" :size="24" color="var(--brand-primary)" class="mb-2" />
          <p class="text-body mb-4">{{ t.text }}</p>
          <p class="text-title" style="font-size: 0.875rem">{{ t.name }}</p>
        </n-card>
      </n-grid-item>
    </n-grid>
  </section>
</template>
