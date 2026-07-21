<script setup lang="ts">
const contactEmail = 'contato@financemind.app'
</script>

<template>
  <v-container id="contato" class="py-12 text-center">
    <h2 class="text-h4 font-weight-bold mb-4">Contato</h2>
    <p class="text-body-1 text-medium-emphasis mb-4">
      Dúvidas, sugestões ou parcerias? Fale com a gente.
    </p>
    <v-btn size="large" color="primary" prepend-icon="mdi-email-outline" :href="`mailto:${contactEmail}`">
      {{ contactEmail }}
    </v-btn>
  </v-container>
</template>
