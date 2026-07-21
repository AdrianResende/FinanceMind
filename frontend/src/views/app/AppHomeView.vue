<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
</script>

<template>
  <v-container>
    <h1 class="text-h5 font-weight-bold mb-2">Bem-vindo(a), {{ auth.user?.full_name }}!</h1>
    <p class="text-body-2 text-medium-emphasis">
      O dashboard completo (patrimônio, rentabilidade, alocação e comparação com benchmarks) chega
      no próximo milestone. Por enquanto, sua conta e autenticação já estão funcionando de ponta a
      ponta.
    </p>
  </v-container>
</template>
