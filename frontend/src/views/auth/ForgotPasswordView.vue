<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

import { authService } from '@/services/authService'

const email = ref('')
const loading = ref(false)
const sent = ref(false)

async function onSubmit() {
  loading.value = true
  try {
    await authService.forgotPassword(email.value)
    sent.value = true
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <v-container class="fill-height auth-bg d-flex align-center justify-center" fluid>
    <v-responsive class="mx-auto" max-width="420">
      <div class="text-center mb-6">
        <RouterLink to="/" class="text-decoration-none text-h5 font-weight-bold text-primary">
          FinanceMind
        </RouterLink>
      </div>
      <v-card class="pa-8" variant="outlined" rounded="lg" elevation="2">
        <h1 class="text-h5 font-weight-bold mb-6 text-center">Recuperar senha</h1>

        <v-alert v-if="sent" type="success" density="compact" class="mb-4">
          Se o email existir em nossa base, um link de redefinição foi enviado.
        </v-alert>

        <v-form v-else @submit.prevent="onSubmit">
          <v-text-field v-model="email" label="Email" type="email" required class="mb-4" />
          <v-btn type="submit" color="primary" block size="large" :loading="loading">
            Enviar link de redefinição
          </v-btn>
        </v-form>

        <div class="text-center mt-4">
          <RouterLink to="/login" class="text-caption">Voltar para o login</RouterLink>
        </div>
      </v-card>
    </v-responsive>
  </v-container>
</template>

<style scoped>
.auth-bg {
  background:
    radial-gradient(circle at 50% 0%, rgba(15, 76, 100, 0.08), transparent 60%),
    #f7f9fa;
}
</style>
