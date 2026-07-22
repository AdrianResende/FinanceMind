<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'

import { useAiChatStore } from '@/stores/aiChat'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const aiChatStore = useAiChatStore()

const fullName = ref(auth.user?.full_name ?? '')
const saving = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

watch(
  () => auth.user?.full_name,
  (value) => {
    fullName.value = value ?? ''
  },
)

onMounted(() => {
  aiChatStore.loadUsage()
})

async function save() {
  if (!fullName.value.trim()) return
  saving.value = true
  successMessage.value = ''
  errorMessage.value = ''
  try {
    await auth.updateProfile(fullName.value.trim())
    successMessage.value = 'Dados atualizados com sucesso.'
  } catch (err) {
    errorMessage.value =
      err instanceof Error && err.message.includes('modo demonstração')
        ? 'Edição de perfil não está disponível no modo demonstração.'
        : 'Não foi possível salvar suas informações. Tente novamente.'
  } finally {
    saving.value = false
  }
}

function formatDate(value: string | undefined) {
  if (!value) return '—'
  return new Date(value).toLocaleDateString('pt-BR', { year: 'numeric', month: 'long' })
}

function usagePct() {
  const usage = aiChatStore.usage
  if (!usage || usage.limit === 0) return 0
  return Math.min(100, Math.round((usage.used / usage.limit) * 100))
}
</script>

<template>
  <div>
    <h1 class="text-section-title mb-6">Perfil</h1>

    <n-grid :x-gap="24" :y-gap="24" cols="1 m:3" responsive="screen">
      <n-grid-item span="1 m:2">
        <n-card title="Dados pessoais" bordered content-style="padding: 24px" class="glass-card">
          <n-form label-placement="top">
            <n-form-item label="Nome completo">
              <n-input v-model:value="fullName" size="large" />
            </n-form-item>
            <n-form-item label="Email">
              <n-input :value="auth.user?.email" disabled size="large" />
            </n-form-item>
          </n-form>

          <n-alert v-if="successMessage" type="success" class="mb-4">{{ successMessage }}</n-alert>
          <n-alert v-if="errorMessage" type="error" class="mb-4">{{ errorMessage }}</n-alert>

          <n-button type="primary" :loading="saving" @click="save">Salvar alterações</n-button>
        </n-card>
      </n-grid-item>

      <n-grid-item span="1">
        <n-card bordered content-style="padding: 24px" class="glass-card mb-6">
          <div class="icon-tile mb-3">
            <MdiIcon name="crown-outline" :size="22" />
          </div>
          <div class="text-muted" style="font-size: 0.8125rem">Plano atual</div>
          <div class="text-title" style="text-transform: capitalize">{{ auth.user?.plan }}</div>
          <div class="text-muted mt-4" style="font-size: 0.8125rem">Membro desde</div>
          <div class="text-body">{{ formatDate(auth.user?.created_at) }}</div>
        </n-card>

        <n-card title="Uso de IA no mês" bordered content-style="padding: 24px" class="glass-card">
          <template v-if="aiChatStore.usage">
            <div class="text-body mb-2">
              {{ aiChatStore.usage.used }} de {{ aiChatStore.usage.limit }} mensagens usadas
            </div>
            <n-progress type="line" :percentage="usagePct()" :height="8" />
          </template>
          <n-skeleton v-else text :repeat="2" />
        </n-card>
      </n-grid-item>
    </n-grid>
  </div>
</template>
