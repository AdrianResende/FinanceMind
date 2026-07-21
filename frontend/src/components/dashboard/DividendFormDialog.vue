<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import type { FormInst, FormRules } from 'naive-ui'

import AssetAutocomplete from '@/components/market/AssetAutocomplete.vue'
import { useDashboardStore } from '@/stores/dashboard'
import type { Asset } from '@/types/asset'

const open = defineModel<boolean>('open', { default: false })

const dashboardStore = useDashboardStore()

const formRef = ref<FormInst | null>(null)
const asset = ref<Asset | null>(null)
const amount = ref<number | null>(null)
const paymentDate = ref<string | null>(null)
const loading = ref(false)
const errorMessage = ref('')

const rules: FormRules = {
  amount: {
    required: true,
    validator: (_rule, value: number | null) =>
      value !== null && value > 0 ? true : new Error('Deve ser maior que zero'),
    trigger: ['blur', 'input'],
  },
  paymentDate: { required: true, message: 'Informe a data do pagamento', trigger: 'blur' },
}

function resetForm() {
  asset.value = null
  amount.value = null
  paymentDate.value = null
  errorMessage.value = ''
}

async function onSubmit() {
  try {
    await formRef.value?.validate()
  } catch {
    return
  }
  if (!asset.value) {
    errorMessage.value = 'Selecione um ativo.'
    return
  }

  errorMessage.value = ''
  loading.value = true
  try {
    await dashboardStore.createDividend({
      asset_id: asset.value.id,
      amount: String(amount.value),
      payment_date: paymentDate.value!,
    })
    open.value = false
    resetForm()
  } catch (err) {
    if (err instanceof Error && err.message.includes('modo demonstração')) {
      errorMessage.value = 'Lançar proventos não está disponível no modo demonstração.'
    } else if (axios.isAxiosError(err)) {
      errorMessage.value = 'Não foi possível salvar o provento. Tente novamente.'
    } else {
      errorMessage.value = 'Não foi possível salvar o provento. Tente novamente.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <n-modal v-model:show="open">
    <n-card
      style="width: 420px"
      title="Lançar provento"
      :bordered="false"
      size="huge"
      role="dialog"
      aria-modal="true"
      content-style="padding-top: 20px"
      class="glass-card glass-card--strong"
    >
      <n-form ref="formRef" :model="{ amount, paymentDate }" :rules="rules">
        <n-form-item label="Ativo">
          <AssetAutocomplete v-model="asset" style="width: 100%" />
        </n-form-item>
        <n-form-item path="amount" label="Valor recebido" show-require-mark>
          <n-input-number
            v-model:value="amount"
            :min="0.01"
            :precision="2"
            style="width: 100%"
            size="large"
          />
        </n-form-item>
        <n-form-item path="paymentDate" label="Data do pagamento" show-require-mark>
          <n-date-picker
            v-model:formatted-value="paymentDate"
            value-format="yyyy-MM-dd"
            type="date"
            style="width: 100%"
            size="large"
          />
        </n-form-item>

        <n-alert v-if="errorMessage" type="error" class="mb-4">{{ errorMessage }}</n-alert>

        <div class="dialog-actions">
          <n-button quaternary @click="open = false">Cancelar</n-button>
          <n-button type="primary" :loading="loading" @click="onSubmit">Salvar</n-button>
        </div>
      </n-form>
    </n-card>
  </n-modal>
</template>

<style scoped>
.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-2);
}
</style>
