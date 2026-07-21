<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute, RouterLink } from 'vue-router'

import { useAuthStore } from '@/stores/auth'
import { authService } from '@/services/authService'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const email = ref('')
const password = ref('')
const loading = ref(false)
const errorMessage = ref('')

async function onSubmit() {
  errorMessage.value = ''
  loading.value = true
  try {
    await auth.login(email.value, password.value)
    const redirect = (route.query.redirect as string) || { name: 'app-home' }
    router.push(redirect)
  } catch {
    errorMessage.value = 'Email ou senha inválidos.'
  } finally {
    loading.value = false
  }
}

function loginWithGoogle() {
  window.location.href = authService.googleLoginUrl()
}
</script>

<template>
  <v-container class="fill-height" fluid>
    <v-responsive class="mx-auto" max-width="420">
      <v-card class="pa-8" variant="outlined">
        <h1 class="text-h5 font-weight-bold mb-6 text-center">Entrar no FinanceMind</h1>

        <v-btn block variant="outlined" prepend-icon="mdi-google" class="mb-4" @click="loginWithGoogle">
          Entrar com Google
        </v-btn>

        <v-divider class="mb-4">
          <span class="text-caption text-medium-emphasis px-2">ou</span>
        </v-divider>

        <v-form @submit.prevent="onSubmit">
          <v-text-field
            v-model="email"
            label="Email"
            type="email"
            required
            class="mb-2"
          />
          <v-text-field
            v-model="password"
            label="Senha"
            type="password"
            required
            class="mb-2"
          />
          <v-alert v-if="errorMessage" type="error" density="compact" class="mb-4">
            {{ errorMessage }}
          </v-alert>
          <v-btn type="submit" color="primary" block size="large" :loading="loading">
            Entrar
          </v-btn>
        </v-form>

        <div class="d-flex justify-space-between mt-4">
          <RouterLink to="/esqueci-senha" class="text-caption">Esqueci minha senha</RouterLink>
          <RouterLink to="/registro" class="text-caption">Criar conta</RouterLink>
        </div>
      </v-card>
    </v-responsive>
  </v-container>
</template>
