<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

import AssetAutocomplete from '@/components/market/AssetAutocomplete.vue'
import { useDashboardStore } from '@/stores/dashboard'
import type { Asset } from '@/types/asset'

const open = defineModel<boolean>('open', { default: false })

const dashboardStore = useDashboardStore()

const asset = ref<Asset | null>(null)
const amount = ref<number | null>(null)
const paymentDate = ref('')
const loading = ref(false)
const errorMessage = ref('')

const positiveRule = (v: number | null) => (v !== null && v > 0) || 'Deve ser maior que zero'
const requiredRule = (v: unknown) => !!v || 'Campo obrigatório'

function resetForm() {
  asset.value = null
  amount.value = null
  paymentDate.value = ''
  errorMessage.value = ''
}

async function onSubmit() {
  if (!asset.value || amount.value === null || !paymentDate.value) {
    return
  }

  errorMessage.value = ''
  loading.value = true
  try {
    await dashboardStore.createDividend({
      asset_id: asset.value.id,
      amount: String(amount.value),
      payment_date: paymentDate.value,
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
  <v-dialog v-model="open" max-width="420">
    <v-card class="pa-4">
      <v-card-title>Lançar provento</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="onSubmit">
          <AssetAutocomplete v-model="asset" class="mb-2" />
          <v-text-field
            v-model.number="amount"
            label="Valor recebido"
            type="number"
            :rules="[requiredRule, positiveRule]"
            class="mb-2"
          />
          <v-text-field
            v-model="paymentDate"
            label="Data do pagamento"
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
