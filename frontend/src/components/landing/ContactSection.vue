<script setup lang="ts">
const contactEmail = 'contato@financemind.app'
</script>

<template>
  <section id="contato" class="page-shell section-py text-center">
    <h2 class="text-section-title mb-4">Contato</h2>
    <p class="text-lead mb-6">Dúvidas, sugestões ou parcerias? Fale com a gente.</p>
    <n-button size="large" type="primary" round tag="a" :href="`mailto:${contactEmail}`">
      <template #icon>
        <MdiIcon name="email-outline" :size="18" />
      </template>
      {{ contactEmail }}
    </n-button>
  </section>
</template>
