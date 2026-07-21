<script setup lang="ts">
import { h, onMounted, ref } from 'vue'
import { NButton, NSpace, NTag, type DataTableColumns } from 'naive-ui'

import MdiIcon from '@/components/common/MdiIcon.vue'
import TransactionFormDialog from '@/components/portfolio/TransactionFormDialog.vue'
import { usePortfolioStore } from '@/stores/portfolio'
import type { PositionItem } from '@/types/portfolio'
import type { Transaction } from '@/types/transaction'

const portfolioStore = usePortfolioStore()

const dialogOpen = ref(false)
const editingTransaction = ref<Transaction | null>(null)

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

function profitColor(value: string) {
  const tone = profitTone(value)
  if (tone === 'success') return 'var(--brand-success)'
  if (tone === 'error') return 'var(--brand-error)'
  return undefined
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

const positionColumns: DataTableColumns<PositionItem> = [
  {
    title: 'Ativo',
    key: 'ticker',
    render: (row) => h('span', { style: 'font-weight: 500' }, row.asset.ticker),
  },
  { title: 'Quantidade', key: 'quantity' },
  { title: 'Preço médio', key: 'avg_price', render: (row) => formatCurrency(row.avg_price) },
  { title: 'Valor investido', key: 'invested_value', render: (row) => formatCurrency(row.invested_value) },
  { title: 'Preço atual', key: 'current_price', render: (row) => formatCurrency(row.current_price) },
  { title: 'Valor atual', key: 'current_value', render: (row) => formatCurrency(row.current_value) },
  {
    title: 'Lucro',
    key: 'profit',
    render: (row) =>
      h(
        'span',
        { style: { color: profitColor(row.profit) } },
        `${formatCurrency(row.profit)} (${formatPercent(row.profit_pct)})`,
      ),
  },
]

const transactionColumns: DataTableColumns<Transaction> = [
  { title: 'Data', key: 'operation_date' },
  {
    title: 'Ativo',
    key: 'ticker',
    render: (row) => h('span', { style: 'font-weight: 500' }, row.asset.ticker),
  },
  {
    title: 'Operação',
    key: 'operation',
    render: (row) =>
      h(
        NTag,
        { type: row.operation === 'compra' ? 'success' : 'error', size: 'small', round: true, bordered: false },
        { default: () => (row.operation === 'compra' ? 'Compra' : 'Venda') },
      ),
  },
  { title: 'Quantidade', key: 'quantity' },
  { title: 'Preço', key: 'unit_price', render: (row) => formatCurrency(row.unit_price) },
  {
    title: 'Ações',
    key: 'actions',
    render: (row) =>
      h(NSpace, { size: 4 }, () => [
        h(
          NButton,
          { quaternary: true, circle: true, size: 'small', onClick: () => openEditDialog(row) },
          { icon: () => h(MdiIcon, { name: 'pencil-outline', size: 16 }) },
        ),
        h(
          NButton,
          { quaternary: true, circle: true, size: 'small', onClick: () => onDelete(row) },
          { icon: () => h(MdiIcon, { name: 'delete-outline', size: 16 }) },
        ),
      ]),
  },
]

onMounted(() => {
  portfolioStore.loadAll()
})
</script>

<template>
  <div>
    <div class="portfolio-header mb-6">
      <h1 class="text-section-title">Carteira</h1>
      <n-button type="primary" round @click="openCreateDialog">
        <template #icon><MdiIcon name="plus" :size="16" /></template>
        Nova transação
      </n-button>
    </div>

    <n-alert v-if="portfolioStore.error" type="error" class="mb-4">
      {{ portfolioStore.error }}
    </n-alert>

    <n-grid v-if="portfolioStore.summary" :x-gap="24" :y-gap="24" cols="1 m:3" responsive="screen" class="mb-6">
      <n-grid-item>
        <n-card bordered hoverable content-style="padding: 24px" class="glass-card stat-card">
          <div class="icon-tile"><MdiIcon name="wallet-outline" :size="22" /></div>
          <div>
            <div class="text-muted" style="font-size: 0.8125rem">Valor investido</div>
            <div class="text-title">{{ formatCurrency(portfolioStore.summary.total_invested) }}</div>
          </div>
        </n-card>
      </n-grid-item>
      <n-grid-item>
        <n-card bordered hoverable content-style="padding: 24px" class="glass-card stat-card">
          <div class="icon-tile"><MdiIcon name="finance" :size="22" /></div>
          <div>
            <div class="text-muted" style="font-size: 0.8125rem">Valor atual</div>
            <div class="text-title">{{ formatCurrency(portfolioStore.summary.total_current) }}</div>
          </div>
        </n-card>
      </n-grid-item>
      <n-grid-item>
        <n-card bordered hoverable content-style="padding: 24px" class="glass-card stat-card">
          <div class="icon-tile">
            <MdiIcon
              :name="Number(portfolioStore.summary.total_profit) >= 0 ? 'trending-up' : 'trending-down'"
              :size="22"
            />
          </div>
          <div>
            <div class="text-muted" style="font-size: 0.8125rem">Lucro</div>
            <div
              class="text-title"
              :style="{ color: profitColor(portfolioStore.summary.total_profit) }"
            >
              {{ formatCurrency(portfolioStore.summary.total_profit) }}
              <span class="text-body">({{ formatPercent(portfolioStore.summary.total_profit_pct) }})</span>
            </div>
          </div>
        </n-card>
      </n-grid-item>
    </n-grid>

    <n-card
      title="Posição consolidada"
      bordered
      content-style="padding: 24px"
      class="glass-card mb-6"
    >
      <n-data-table
        :columns="positionColumns"
        :data="portfolioStore.summary?.positions ?? []"
        :loading="portfolioStore.loading"
        :bordered="false"
      >
        <template #empty>Nenhuma posição ainda. Lance sua primeira transação.</template>
      </n-data-table>
    </n-card>

    <n-card title="Transações" bordered content-style="padding: 24px" class="glass-card">
      <n-data-table
        :columns="transactionColumns"
        :data="portfolioStore.transactions"
        :loading="portfolioStore.loading"
        :bordered="false"
      >
        <template #empty>Nenhuma transação lançada ainda.</template>
      </n-data-table>
    </n-card>

    <TransactionFormDialog v-model:open="dialogOpen" :editing-transaction="editingTransaction" />
  </div>
</template>

<style scoped>
.portfolio-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.stat-card :deep(.n-card__content) {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}
</style>
