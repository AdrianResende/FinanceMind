<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import type { FormInst, FormRules } from 'naive-ui'

import { authService } from '@/services/authService'

const route = useRoute()
const router = useRouter()

const formRef = ref<FormInst | null>(null)
const newPassword = ref('')
const loading = ref(false)
const errorMessage = ref('')
const success = ref(false)

const rules: FormRules = {
  newPassword: {
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
  <div class="auth-page">
    <div class="auth-wrap">
      <RouterLink to="/" class="auth-brand text-title mb-6">FinanceMind</RouterLink>

      <n-card bordered content-style="padding: 32px" class="glass-card glass-card--strong">
        <h1 class="text-title text-center mb-6">Redefinir senha</h1>

        <n-alert v-if="success" type="success" class="mb-4">
          Senha redefinida! Redirecionando para o login...
        </n-alert>

        <n-form
          v-else
          ref="formRef"
          :model="{ newPassword }"
          :rules="rules"
          @submit.prevent="onSubmit"
        >
          <n-form-item path="newPassword" label="Nova senha" show-require-mark>
            <n-input
              v-model:value="newPassword"
              type="password"
              placeholder="Mínimo 8 caracteres"
              size="large"
              show-password-on="click"
            />
          </n-form-item>
          <n-alert v-if="errorMessage" type="error" class="mb-4">{{ errorMessage }}</n-alert>
          <n-button type="primary" block size="large" attr-type="submit" :loading="loading">
            Redefinir senha
          </n-button>
        </n-form>
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
