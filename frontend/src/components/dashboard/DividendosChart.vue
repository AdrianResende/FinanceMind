<script setup lang="ts">
import { computed, ref } from 'vue'
import type { ApexOptions } from 'apexcharts'

import DividendFormDialog from '@/components/dashboard/DividendFormDialog.vue'
import { ApexChart } from '@/plugins/apexchart'
import { useDashboardStore } from '@/stores/dashboard'
import type { Dividend } from '@/types/dividend'

const props = defineProps<{
  dividends: Dividend[]
}>()

const dashboardStore = useDashboardStore()
const dialogOpen = ref(false)

function formatCurrency(value: number) {
  return value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

const monthlyTotals = computed(() => {
  const totals = new Map<string, number>()
  for (const dividend of props.dividends) {
    const month = dividend.payment_date.slice(0, 7)
    totals.set(month, (totals.get(month) ?? 0) + Number(dividend.amount))
  }
  return [...totals.entries()].sort(([a], [b]) => a.localeCompare(b))
})

const series = computed(() => [
  { name: 'Dividendos', data: monthlyTotals.value.map(([, total]) => total) },
])

const options = computed<ApexOptions>(() => ({
  chart: { type: 'bar', toolbar: { show: false } },
  xaxis: { categories: monthlyTotals.value.map(([month]) => month) },
  dataLabels: { enabled: false },
  colors: ['#0E9C8F'],
}))

async function onDelete(id: string) {
  await dashboardStore.deleteDividend(id)
}
</script>

<template>
  <n-card bordered hoverable content-style="padding: 24px" class="glass-card">
    <template #header>Dividendos recebidos</template>
    <template #header-extra>
      <n-button size="small" type="primary" round @click="dialogOpen = true">
        <template #icon><MdiIcon name="plus" :size="16" /></template>
        Lançar provento
      </n-button>
    </template>

    <ApexChart v-if="monthlyTotals.length" type="bar" height="240" :options="options" :series="series" />
    <p v-else class="text-body">Nenhum provento lançado ainda.</p>

    <div v-if="dividends.length" class="dividend-list mt-4">
      <div v-for="dividend in dividends" :key="dividend.id" class="dividend-row">
        <div>
          <div class="text-body" style="font-weight: 500">
            {{ dividend.asset.ticker }} · {{ formatCurrency(Number(dividend.amount)) }}
          </div>
          <div class="text-muted" style="font-size: 0.8125rem">{{ dividend.payment_date }}</div>
        </div>
        <n-button quaternary circle size="small" @click="onDelete(dividend.id)">
          <template #icon><MdiIcon name="delete-outline" :size="16" /></template>
        </n-button>
      </div>
    </div>

    <DividendFormDialog v-model:open="dialogOpen" />
  </n-card>
</template>

<style scoped>
.dividend-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.dividend-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-block: var(--space-2);
  border-bottom: 1px solid rgba(15, 76, 100, 0.08);
}

.dividend-row:last-child {
  border-bottom: none;
}
</style>
