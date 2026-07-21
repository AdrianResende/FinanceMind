<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'

import { authService } from '@/services/authService'

const route = useRoute()
const router = useRouter()

const newPassword = ref('')
const loading = ref(false)
const errorMessage = ref('')
const success = ref(false)

async function onSubmit() {
  errorMessage.value = ''
  loading.value = true
  try {
    const token = route.query.token as string
    await authService.resetPassword({ token, new_password: newPassword.value })
    success.value = true
    setTimeout(() => router.push({ name: 'login' }), 2000)
  } catch {
    errorMessage.value = 'Link inválido ou expirado. Solicite uma nova redefinição.'
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
        <h1 class="text-h5 font-weight-bold mb-6 text-center">Redefinir senha</h1>

        <v-alert v-if="success" type="success" density="compact" class="mb-4">
          Senha redefinida! Redirecionando para o login...
        </v-alert>

        <v-form v-else @submit.prevent="onSubmit">
          <v-text-field
            v-model="newPassword"
            label="Nova senha"
            type="password"
            hint="Mínimo 8 caracteres"
            required
            class="mb-4"
          />
          <v-alert v-if="errorMessage" type="error" density="compact" class="mb-4">
            {{ errorMessage }}
          </v-alert>
          <v-btn type="submit" color="primary" block size="large" :loading="loading">
            Redefinir senha
          </v-btn>
        </v-form>
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
