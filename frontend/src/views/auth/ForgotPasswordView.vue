<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import type { FormInst, FormRules } from 'naive-ui'

import { authService } from '@/services/authService'

const formRef = ref<FormInst | null>(null)
const email = ref('')
const loading = ref(false)
const sent = ref(false)

const rules: FormRules = {
  email: { required: true, message: 'Informe seu email', trigger: 'blur' },
}

async function onSubmit() {
  try {
    await formRef.value?.validate()
  } catch {
    return
  }
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
  <div class="auth-page">
    <div class="auth-wrap">
      <RouterLink to="/" class="auth-brand text-title mb-6">FinanceMind</RouterLink>

      <n-card bordered content-style="padding: 32px" class="glass-card glass-card--strong">
        <h1 class="text-title text-center mb-6">Recuperar senha</h1>

        <n-alert v-if="sent" type="success" class="mb-4">
          Se o email existir em nossa base, um link de redefinição foi enviado.
        </n-alert>

        <n-form v-else ref="formRef" :model="{ email }" :rules="rules" @submit.prevent="onSubmit">
          <n-form-item path="email" label="Email" show-require-mark>
            <n-input v-model:value="email" placeholder="voce@email.com" size="large" />
          </n-form-item>
          <n-button type="primary" block size="large" attr-type="submit" :loading="loading">
            Enviar link de redefinição
          </n-button>
        </n-form>

        <div class="text-center mt-4">
          <RouterLink to="/login" class="text-body">Voltar para o login</RouterLink>
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
