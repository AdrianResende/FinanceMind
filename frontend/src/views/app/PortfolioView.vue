<script setup lang="ts">
import { onMounted, ref } from 'vue'

import TransactionFormDialog from '@/components/portfolio/TransactionFormDialog.vue'
import { usePortfolioStore } from '@/stores/portfolio'
import type { Transaction } from '@/types/transaction'

const portfolioStore = usePortfolioStore()

const dialogOpen = ref(false)
const editingTransaction = ref<Transaction | null>(null)

const positionHeaders = [
  { title: 'Ativo', key: 'ticker' },
  { title: 'Quantidade', key: 'quantity' },
  { title: 'Preço médio', key: 'avg_price' },
  { title: 'Valor investido', key: 'invested_value' },
  { title: 'Preço atual', key: 'current_price' },
  { title: 'Valor atual', key: 'current_value' },
  { title: 'Lucro', key: 'profit' },
]

const transactionHeaders = [
  { title: 'Data', key: 'operation_date' },
  { title: 'Ativo', key: 'ticker' },
  { title: 'Operação', key: 'operation' },
  { title: 'Quantidade', key: 'quantity' },
  { title: 'Preço', key: 'unit_price' },
  { title: 'Ações', key: 'actions', sortable: false },
]

function formatCurrency(value: string) {
  return Number(value).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

function formatPercent(value: string) {
  const sign = Number(value) > 0 ? '+' : ''
  return `${sign}${Number(value).toFixed(2)}%`
}

function profitTone(value: string): 'success' | 'error' | undefined {
  const n = Number(value)
  if (n > 0) return 'success'
  if (n < 0) return 'error'
  return undefined
}

function profitClass(value: string) {
  const tone = profitTone(value)
  return tone ? `text-${tone}` : ''
}

function openCreateDialog() {
  editingTransaction.value = null
  dialogOpen.value = true
}

function openEditDialog(transaction: Transaction) {
  editingTransaction.value = transaction
  dialogOpen.value = true
}

async function onDelete(transaction: Transaction) {
  await portfolioStore.deleteTransaction(transaction.id)
}

onMounted(() => {
  portfolioStore.loadAll()
})
</script>

<template>
  <v-container>
    <div class="d-flex align-center justify-space-between mb-4">
      <h1 class="text-h5 font-weight-bold">Carteira</h1>
      <v-btn color="primary" prepend-icon="mdi-plus" @click="openCreateDialog">Nova transação</v-btn>
    </div>

    <v-alert v-if="portfolioStore.error" type="error" density="compact" class="mb-4">
      {{ portfolioStore.error }}
    </v-alert>

    <v-row v-if="portfolioStore.summary" class="mb-2">
      <v-col cols="12" sm="4">
        <v-card class="pa-4 d-flex align-center ga-3">
          <v-avatar color="primary" variant="tonal" icon="mdi-wallet-outline" />
          <div>
            <div class="text-caption text-medium-emphasis">Valor investido</div>
            <div class="text-h6">{{ formatCurrency(portfolioStore.summary.total_invested) }}</div>
          </div>
        </v-card>
      </v-col>
      <v-col cols="12" sm="4">
        <v-card class="pa-4 d-flex align-center ga-3">
          <v-avatar color="primary" variant="tonal" icon="mdi-finance" />
          <div>
            <div class="text-caption text-medium-emphasis">Valor atual</div>
            <div class="text-h6">{{ formatCurrency(portfolioStore.summary.total_current) }}</div>
          </div>
        </v-card>
      </v-col>
      <v-col cols="12" sm="4">
        <v-card class="pa-4 d-flex align-center ga-3">
          <v-avatar
            :color="profitTone(portfolioStore.summary.total_profit) ?? 'primary'"
            variant="tonal"
            :icon="Number(portfolioStore.summary.total_profit) >= 0 ? 'mdi-trending-up' : 'mdi-trending-down'"
          />
          <div>
            <div class="text-caption text-medium-emphasis">Lucro</div>
            <div class="text-h6" :class="profitClass(portfolioStore.summary.total_profit)">
              {{ formatCurrency(portfolioStore.summary.total_profit) }}
              <span class="text-body-2">({{ formatPercent(portfolioStore.summary.total_profit_pct) }})</span>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <v-card class="mb-6">
      <v-card-title>Posição consolidada</v-card-title>
      <v-data-table
        :headers="positionHeaders"
        :items="portfolioStore.summary?.positions ?? []"
        :loading="portfolioStore.loading"
        no-data-text="Nenhuma posição ainda. Lance sua primeira transação."
      >
        <template #item="{ item }">
          <tr>
            <td class="font-weight-medium">{{ item.asset.ticker }}</td>
            <td>{{ item.quantity }}</td>
            <td>{{ formatCurrency(item.avg_price) }}</td>
            <td>{{ formatCurrency(item.invested_value) }}</td>
            <td>{{ formatCurrency(item.current_price) }}</td>
            <td>{{ formatCurrency(item.current_value) }}</td>
            <td :class="profitClass(item.profit)">
              {{ formatCurrency(item.profit) }} ({{ formatPercent(item.profit_pct) }})
            </td>
          </tr>
        </template>
      </v-data-table>
    </v-card>

    <v-card>
      <v-card-title>Transações</v-card-title>
      <v-data-table
        :headers="transactionHeaders"
        :items="portfolioStore.transactions"
        :loading="portfolioStore.loading"
        no-data-text="Nenhuma transação lançada ainda."
      >
        <template #item="{ item }">
          <tr>
            <td>{{ item.operation_date }}</td>
            <td class="font-weight-medium">{{ item.asset.ticker }}</td>
            <td>
              <v-chip
                size="small"
                :color="item.operation === 'compra' ? 'success' : 'error'"
                variant="tonal"
              >
                {{ item.operation === 'compra' ? 'Compra' : 'Venda' }}
              </v-chip>
            </td>
            <td>{{ item.quantity }}</td>
            <td>{{ formatCurrency(item.unit_price) }}</td>
            <td>
              <v-btn icon="mdi-pencil" variant="text" size="small" @click="openEditDialog(item)" />
              <v-btn icon="mdi-delete" variant="text" size="small" @click="onDelete(item)" />
            </td>
          </tr>
        </template>
      </v-data-table>
    </v-card>

    <TransactionFormDialog v-model:open="dialogOpen" :editing-transaction="editingTransaction" />
  </v-container>
</template>
