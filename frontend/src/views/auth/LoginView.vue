<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute, RouterLink } from 'vue-router'
import type { FormInst, FormRules } from 'naive-ui'

import { useAuthStore } from '@/stores/auth'
import { authService } from '@/services/authService'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const formRef = ref<FormInst | null>(null)
const email = ref('')
const password = ref('')
const loading = ref(false)
const errorMessage = ref('')

const rules: FormRules = {
  email: { required: true, message: 'Informe seu email', trigger: 'blur' },
  password: { required: true, message: 'Informe sua senha', trigger: 'blur' },
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

const showDemoLogin = import.meta.env.DEV

function enterDemoMode() {
  auth.enterDemoMode()
  router.push({ name: 'portfolio-home' })
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-wrap">
      <RouterLink to="/" class="auth-brand text-title mb-6">FinanceMind</RouterLink>

      <n-card bordered content-style="padding: 32px" class="glass-card glass-card--strong">
        <h1 class="text-title text-center mb-6">Entrar no FinanceMind</h1>

        <n-button block secondary size="large" class="mb-4" @click="loginWithGoogle">
          <template #icon><MdiIcon name="google" :size="18" /></template>
          Entrar com Google
        </n-button>

        <n-divider class="mb-4">ou</n-divider>

        <n-form ref="formRef" :model="{ email, password }" :rules="rules" @submit.prevent="onSubmit">
          <n-form-item path="email" label="Email" show-require-mark>
            <n-input v-model:value="email" type="text" placeholder="voce@email.com" size="large" />
          </n-form-item>
          <n-form-item path="password" label="Senha" show-require-mark>
            <n-input
              v-model:value="password"
              type="password"
              placeholder="••••••••"
              size="large"
              show-password-on="click"
            />
          </n-form-item>
          <n-alert v-if="errorMessage" type="error" class="mb-4">{{ errorMessage }}</n-alert>
          <n-button type="primary" block size="large" attr-type="submit" :loading="loading">
            Entrar
          </n-button>
        </n-form>

        <div class="auth-links mt-4">
          <RouterLink to="/esqueci-senha" class="text-body">Esqueci minha senha</RouterLink>
          <RouterLink to="/registro" class="text-body">Criar conta</RouterLink>
        </div>

        <template v-if="showDemoLogin">
          <n-divider class="my-4">dev</n-divider>
          <n-button block secondary type="warning" @click="enterDemoMode">
            <template #icon><MdiIcon name="flask-outline" :size="18" /></template>
            Entrar em modo demonstração
          </n-button>
          <p class="text-muted text-center mt-2" style="font-size: 0.8rem">
            Sem backend/banco — navega com dados fictícios. Só aparece em build de desenvolvimento.
          </p>
        </template>
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

.auth-links {
  display: flex;
  justify-content: space-between;
}
</style>
