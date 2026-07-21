<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<template>
  <v-container class="py-16 text-center">
    <v-responsive class="mx-auto" max-width="720">
      <h1 class="text-h3 text-md-h2 font-weight-bold mb-4">
        Entenda seus investimentos. Acompanhe sua carteira. Cresça com confiança.
      </h1>
      <p class="text-body-1 text-medium-emphasis mb-8">
        FinanceMind ensina como funcionam Ações, FIIs, ETFs, Tesouro Direto e outros investimentos,
        e ajuda você a acompanhar sua carteira com clareza — sem jargão, sem achismo.
      </p>
      <div class="d-flex justify-center ga-4 flex-wrap">
        <v-btn size="large" color="primary" @click="router.push({ name: 'register' })">
          Criar conta grátis
        </v-btn>
        <v-btn size="large" variant="outlined" href="#recursos"> Ver recursos </v-btn>
      </div>
      <p class="text-caption text-medium-emphasis mt-4">
        Conteúdo educativo. Não é recomendação de investimento.
      </p>
    </v-responsive>
  </v-container>
</template>
