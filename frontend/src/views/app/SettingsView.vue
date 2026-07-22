<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import type { FormInst, FormRules } from 'naive-ui'

import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()

const formRef = ref<FormInst | null>(null)
const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const savingPassword = ref(false)
const passwordSuccess = ref('')
const passwordError = ref('')

const deleting = ref(false)
const deleteError = ref('')

const rules: FormRules = {
  currentPassword: { required: true, message: 'Informe sua senha atual', trigger: 'blur' },
  newPassword: { required: true, min: 8, message: 'Mínimo de 8 caracteres', trigger: ['blur', 'input'] },
  confirmPassword: {
    required: true,
    validator: (_rule, value: string) =>
      value === newPassword.value ? true : new Error('As senhas não coincidem'),
    trigger: ['blur', 'input'],
  },
}

async function changePassword() {
  try {
    await formRef.value?.validate()
  } catch {
    return
  }

  passwordSuccess.value = ''
  passwordError.value = ''
  savingPassword.value = true
  try {
    await auth.changePassword(currentPassword.value, newPassword.value)
    passwordSuccess.value = 'Senha alterada com sucesso.'
    currentPassword.value = ''
    newPassword.value = ''
    confirmPassword.value = ''
  } catch (err) {
    if (err instanceof Error && err.message.includes('modo demonstração')) {
      passwordError.value = 'Troca de senha não está disponível no modo demonstração.'
    } else {
      passwordError.value = 'Não foi possível alterar a senha. Verifique a senha atual e tente novamente.'
    }
  } finally {
    savingPassword.value = false
  }
}

async function confirmDeleteAccount() {
  deleteError.value = ''
  deleting.value = true
  try {
    await auth.deleteAccount()
    router.push({ name: 'landing' })
  } catch (err) {
    deleting.value = false
    deleteError.value =
      err instanceof Error && err.message.includes('modo demonstração')
        ? 'Exclusão de conta não está disponível no modo demonstração.'
        : 'Não foi possível excluir sua conta. Tente novamente.'
  }
}
</script>

<template>
  <div>
    <h1 class="text-section-title mb-6">Configurações</h1>

    <n-grid :x-gap="24" :y-gap="24" cols="1 m:2" responsive="screen">
      <n-grid-item>
        <n-card title="Segurança" bordered content-style="padding: 24px" class="glass-card mb-6">
          <template v-if="auth.user?.auth_provider === 'local'">
            <n-form
              ref="formRef"
              :model="{ currentPassword, newPassword, confirmPassword }"
              :rules="rules"
              label-placement="top"
            >
              <n-form-item path="currentPassword" label="Senha atual">
                <n-input v-model:value="currentPassword" type="password" show-password-on="click" size="large" />
              </n-form-item>
              <n-form-item path="newPassword" label="Nova senha">
                <n-input v-model:value="newPassword" type="password" show-password-on="click" size="large" />
              </n-form-item>
              <n-form-item path="confirmPassword" label="Confirmar nova senha">
                <n-input v-model:value="confirmPassword" type="password" show-password-on="click" size="large" />
              </n-form-item>

              <n-alert v-if="passwordSuccess" type="success" class="mb-4">{{ passwordSuccess }}</n-alert>
              <n-alert v-if="passwordError" type="error" class="mb-4">{{ passwordError }}</n-alert>

              <n-button type="primary" :loading="savingPassword" @click="changePassword">
                Alterar senha
              </n-button>
            </n-form>
          </template>
          <template v-else>
            <p class="text-body">
              Sua conta está vinculada ao Google — não há senha local para gerenciar por aqui.
            </p>
          </template>
        </n-card>

        <n-card title="Assinatura" bordered content-style="padding: 24px" class="glass-card">
          <p class="text-body mb-4">
            Plano atual: <strong style="text-transform: capitalize">{{ auth.user?.plan }}</strong>
          </p>
          <n-tooltip trigger="hover">
            <template #trigger>
              <n-button disabled>Gerenciar assinatura (em breve)</n-button>
            </template>
            O portal de assinatura chega em uma próxima etapa do produto.
          </n-tooltip>
        </n-card>
      </n-grid-item>

      <n-grid-item>
        <n-card title="Conta" bordered content-style="padding: 24px" class="glass-card">
          <p class="text-body mb-4">
            Excluir sua conta remove permanentemente seus dados de carteira, transações e conversas de IA. Essa
            ação não pode ser desfeita.
          </p>
          <n-alert v-if="deleteError" type="error" class="mb-4">{{ deleteError }}</n-alert>
          <n-popconfirm @positive-click="confirmDeleteAccount">
            <template #trigger>
              <n-button type="error" secondary :loading="deleting">
                <template #icon><MdiIcon name="delete-outline" :size="18" /></template>
                Excluir conta
              </n-button>
            </template>
            Tem certeza que deseja excluir sua conta permanentemente?
          </n-popconfirm>
        </n-card>
      </n-grid-item>
    </n-grid>
  </div>
</template>
