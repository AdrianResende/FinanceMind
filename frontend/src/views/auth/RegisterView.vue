<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import axios from 'axios'

import { useAuthStore } from '@/stores/auth'
import { authService } from '@/services/authService'

const router = useRouter()
const auth = useAuthStore()

const fullName = ref('')
const email = ref('')
const password = ref('')
const loading = ref(false)
const errorMessage = ref('')

async function onSubmit() {
  errorMessage.value = ''
  loading.value = true
  try {
    await auth.register(email.value, password.value, fullName.value)
    router.push({ name: 'app-home' })
  } catch (err) {
    if (axios.isAxiosError(err) && err.response?.status === 409) {
      errorMessage.value = 'Este email já está cadastrado.'
    } else {
      errorMessage.value = 'Não foi possível criar sua conta. Tente novamente.'
    }
  } finally {
    loading.value = false
  }
}

function registerWithGoogle() {
  window.location.href = authService.googleLoginUrl()
}
</script>

<template>
  <v-container class="fill-height" fluid>
    <v-responsive class="mx-auto" max-width="420">
      <v-card class="pa-8" variant="outlined">
        <h1 class="text-h5 font-weight-bold mb-6 text-center">Criar conta grátis</h1>

        <v-btn block variant="outlined" prepend-icon="mdi-google" class="mb-4" @click="registerWithGoogle">
          Cadastrar com Google
        </v-btn>

        <v-divider class="mb-4">
          <span class="text-caption text-medium-emphasis px-2">ou</span>
        </v-divider>

        <v-form @submit.prevent="onSubmit">
          <v-text-field v-model="fullName" label="Nome completo" required class="mb-2" />
          <v-text-field v-model="email" label="Email" type="email" required class="mb-2" />
          <v-text-field
            v-model="password"
            label="Senha"
            type="password"
            required
            hint="Mínimo 8 caracteres"
            class="mb-2"
          />
          <v-alert v-if="errorMessage" type="error" density="compact" class="mb-4">
            {{ errorMessage }}
          </v-alert>
          <v-btn type="submit" color="primary" block size="large" :loading="loading">
            Criar conta
          </v-btn>
        </v-form>

        <div class="text-center mt-4">
          <RouterLink to="/login" class="text-caption">Já tenho conta</RouterLink>
        </div>
      </v-card>
    </v-responsive>
  </v-container>
</template>
