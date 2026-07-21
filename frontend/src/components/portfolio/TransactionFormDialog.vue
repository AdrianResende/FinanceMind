<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import axios from 'axios'

import AssetAutocomplete from '@/components/market/AssetAutocomplete.vue'
import { usePortfolioStore } from '@/stores/portfolio'
import type { Asset } from '@/types/asset'
import type { Transaction, TransactionOperation } from '@/types/transaction'

const open = defineModel<boolean>('open', { default: false })

const props = defineProps<{
  editingTransaction?: Transaction | null
}>()

const portfolioStore = usePortfolioStore()

const asset = ref<Asset | null>(null)
const operation = ref<TransactionOperation>('compra')
const quantity = ref<number | null>(null)
const unitPrice = ref<number | null>(null)
const fees = ref<number | null>(0)
const operationDate = ref('')
const loading = ref(false)
const errorMessage = ref('')

const isEditing = computed(() => !!props.editingTransaction)

const operationOptions = [
  { title: 'Compra', value: 'compra' },
  { title: 'Venda', value: 'venda' },
]

const positiveRule = (v: number | null) => (v !== null && v > 0) || 'Deve ser maior que zero'
const requiredRule = (v: unknown) => !!v || 'Campo obrigatório'

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
      operationDate.value = ''
    }
    errorMessage.value = ''
  },
  { immediate: true },
)

async function onSubmit() {
  if (!asset.value || quantity.value === null || unitPrice.value === null) {
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
      operation_date: operationDate.value,
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
  <v-dialog v-model="open" max-width="480">
    <v-card class="pa-4">
      <v-card-title>{{ isEditing ? 'Editar transação' : 'Nova transação' }}</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="onSubmit">
          <AssetAutocomplete v-model="asset" :disabled="isEditing" class="mb-2" />
          <v-select
            v-model="operation"
            :items="operationOptions"
            label="Operação"
            required
            class="mb-2"
          />
          <v-text-field
            v-model.number="quantity"
            label="Quantidade"
            type="number"
            :rules="[requiredRule, positiveRule]"
            class="mb-2"
          />
          <v-text-field
            v-model.number="unitPrice"
            label="Preço unitário"
            type="number"
            :rules="[requiredRule, positiveRule]"
            class="mb-2"
          />
          <v-text-field v-model.number="fees" label="Taxas" type="number" class="mb-2" />
          <v-text-field
            v-model="operationDate"
            label="Data da operação"
            type="date"
            :rules="[requiredRule]"
            class="mb-2"
          />

          <v-alert v-if="errorMessage" type="error" density="compact" class="mb-4">
            {{ errorMessage }}
          </v-alert>

          <v-card-actions class="px-0">
            <v-spacer />
            <v-btn variant="text" @click="open = false">Cancelar</v-btn>
            <v-btn type="submit" color="primary" :loading="loading">Salvar</v-btn>
          </v-card-actions>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
