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
  <v-container id="depoimentos" class="py-12">
    <h2 class="text-h4 font-weight-bold text-center mb-2">O que dizem sobre o FinanceMind</h2>
    <p class="text-caption text-medium-emphasis text-center mb-10">
      Depoimentos ilustrativos — serão substituídos por relatos reais de usuários assim que o
      programa beta tiver feedback suficiente.
    </p>
    <v-row>
      <v-col v-for="t in testimonials" :key="t.name" cols="12" md="4">
        <v-card class="pa-6 h-100" variant="outlined">
          <v-icon icon="mdi-format-quote-open" color="primary" class="mb-2" />
          <p class="text-body-2 mb-4">{{ t.text }}</p>
          <p class="text-caption font-weight-bold">{{ t.name }}</p>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
