<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import axios from 'axios'
import type { FormInst, FormRules, SelectOption } from 'naive-ui'

import AssetAutocomplete from '@/components/market/AssetAutocomplete.vue'
import { usePortfolioStore } from '@/stores/portfolio'
import type { Asset } from '@/types/asset'
import type { Transaction, TransactionOperation } from '@/types/transaction'

const open = defineModel<boolean>('open', { default: false })

const props = defineProps<{
  editingTransaction?: Transaction | null
}>()

const portfolioStore = usePortfolioStore()

const formRef = ref<FormInst | null>(null)
const asset = ref<Asset | null>(null)
const operation = ref<TransactionOperation>('compra')
const quantity = ref<number | null>(null)
const unitPrice = ref<number | null>(null)
const fees = ref<number | null>(0)
const operationDate = ref<string | null>(null)
const loading = ref(false)
const errorMessage = ref('')

const isEditing = computed(() => !!props.editingTransaction)

const operationOptions: SelectOption[] = [
  { label: 'Compra', value: 'compra' },
  { label: 'Venda', value: 'venda' },
]

const rules: FormRules = {
  quantity: {
    required: true,
    validator: (_rule, value: number | null) =>
      value !== null && value > 0 ? true : new Error('Deve ser maior que zero'),
    trigger: ['blur', 'input'],
  },
  unitPrice: {
    required: true,
    validator: (_rule, value: number | null) =>
      value !== null && value > 0 ? true : new Error('Deve ser maior que zero'),
    trigger: ['blur', 'input'],
  },
  operationDate: { required: true, message: 'Informe a data da operação', trigger: 'blur' },
}

watch(
  () => props.editingTransaction,
  (transaction) => {
    if (transaction) {
      asset.value = transaction.asset
      operation.value = transaction.operation
      quantity.value = Number(transaction.quantity)
      unitPrice.value = Number(transaction.unit_price)
      fees.value = Number(transaction.fees)
      operationDate.value = transaction.operation_date
    } else {
      asset.value = null
      operation.value = 'compra'
      quantity.value = null
      unitPrice.value = null
      fees.value = 0
      operationDate.value = null
    }
    errorMessage.value = ''
  },
  { immediate: true },
)

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
    const payload = {
      asset_id: asset.value.id,
      operation: operation.value,
      quantity: String(quantity.value),
      unit_price: String(unitPrice.value),
      fees: String(fees.value ?? 0),
      operation_date: operationDate.value!,
    }

    if (isEditing.value && props.editingTransaction) {
      await portfolioStore.updateTransaction(props.editingTransaction.id, payload)
    } else {
      await portfolioStore.createTransaction(payload)
    }
    open.value = false
  } catch (err) {
    if (axios.isAxiosError(err) && err.response?.status === 400) {
      errorMessage.value = 'Quantidade insuficiente do ativo para realizar a venda.'
    } else if (err instanceof Error && err.message.includes('modo demonstração')) {
      errorMessage.value = 'Lançar transações não está disponível no modo demonstração.'
    } else {
      errorMessage.value = 'Não foi possível salvar a transação. Tente novamente.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <n-modal v-model:show="open">
    <n-card
      style="width: 480px"
      :title="isEditing ? 'Editar transação' : 'Nova transação'"
      :bordered="false"
      size="huge"
      role="dialog"
      aria-modal="true"
      content-style="padding-top: 20px"
      class="glass-card glass-card--strong"
    >
      <n-form ref="formRef" :model="{ quantity, unitPrice, operationDate }" :rules="rules">
        <n-form-item label="Ativo">
          <AssetAutocomplete v-model="asset" :disabled="isEditing" style="width: 100%" />
        </n-form-item>
        <n-form-item label="Operação">
          <n-select v-model:value="operation" :options="operationOptions" size="large" />
        </n-form-item>
        <n-form-item path="quantity" label="Quantidade" show-require-mark>
          <n-input-number v-model:value="quantity" :min="0.000001" style="width: 100%" size="large" />
        </n-form-item>
        <n-form-item path="unitPrice" label="Preço unitário" show-require-mark>
          <n-input-number
            v-model:value="unitPrice"
            :min="0.01"
            :precision="2"
            style="width: 100%"
            size="large"
          />
        </n-form-item>
        <n-form-item label="Taxas">
          <n-input-number v-model:value="fees" :min="0" :precision="2" style="width: 100%" size="large" />
        </n-form-item>
        <n-form-item path="operationDate" label="Data da operação" show-require-mark>
          <n-date-picker
            v-model:formatted-value="operationDate"
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
