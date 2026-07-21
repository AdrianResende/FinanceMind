<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import axios from 'axios'
import type { FormInst, FormRules } from 'naive-ui'

import { useAuthStore } from '@/stores/auth'
import { authService } from '@/services/authService'

const router = useRouter()
const auth = useAuthStore()

const formRef = ref<FormInst | null>(null)
const fullName = ref('')
const email = ref('')
const password = ref('')
const loading = ref(false)
const errorMessage = ref('')

const rules: FormRules = {
  fullName: { required: true, message: 'Informe seu nome', trigger: 'blur' },
  email: { required: true, message: 'Informe seu email', trigger: 'blur' },
  password: {
    required: true,
    min: 8,
    message: 'Mínimo de 8 caracteres',
    trigger: ['blur', 'input'],
  },
}

async function onSubmit() {
  errorMessage.value = ''
  try {
    await formRef.value?.validate()
  } catch {
    return
  }
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
  <div class="auth-page">
    <div class="auth-wrap">
      <RouterLink to="/" class="auth-brand text-title mb-6">FinanceMind</RouterLink>

      <n-card bordered content-style="padding: 32px" class="glass-card glass-card--strong">
        <h1 class="text-title text-center mb-6">Criar conta grátis</h1>

        <n-button block secondary size="large" class="mb-4" @click="registerWithGoogle">
          <template #icon><MdiIcon name="google" :size="18" /></template>
          Cadastrar com Google
        </n-button>

        <n-divider class="mb-4">ou</n-divider>

        <n-form ref="formRef" :model="{ fullName, email, password }" :rules="rules" @submit.prevent="onSubmit">
          <n-form-item path="fullName" label="Nome completo" show-require-mark>
            <n-input v-model:value="fullName" placeholder="Seu nome" size="large" />
          </n-form-item>
          <n-form-item path="email" label="Email" show-require-mark>
            <n-input v-model:value="email" placeholder="voce@email.com" size="large" />
          </n-form-item>
          <n-form-item path="password" label="Senha" show-require-mark>
            <n-input
              v-model:value="password"
              type="password"
              placeholder="Mínimo 8 caracteres"
              size="large"
              show-password-on="click"
            />
          </n-form-item>
          <n-alert v-if="errorMessage" type="error" class="mb-4">{{ errorMessage }}</n-alert>
          <n-button type="primary" block size="large" attr-type="submit" :loading="loading">
            Criar conta
          </n-button>
        </n-form>

        <div class="text-center mt-4">
          <RouterLink to="/login" class="text-body">Já tenho conta</RouterLink>
        </div>
      </n-card>
    </div>
  </div>
</template>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-6);
}

.auth-wrap {
  width: 100%;
  max-width: 420px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.auth-brand {
  color: var(--brand-primary);
  text-decoration: none;
}
</style>
