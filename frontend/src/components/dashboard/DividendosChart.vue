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
  <v-card class="pa-4">
    <div class="d-flex align-center justify-space-between mb-2">
      <v-card-title class="pa-0">Dividendos recebidos</v-card-title>
      <v-btn size="small" color="primary" prepend-icon="mdi-plus" @click="dialogOpen = true">
        Lançar provento
      </v-btn>
    </div>

    <ApexChart v-if="monthlyTotals.length" type="bar" height="240" :options="options" :series="series" />
    <p v-else class="text-body-2 text-medium-emphasis pa-4">Nenhum provento lançado ainda.</p>

    <v-list v-if="dividends.length" density="compact" class="mt-2">
      <v-list-item v-for="dividend in dividends" :key="dividend.id" :title="`${dividend.asset.ticker} · ${formatCurrency(Number(dividend.amount))}`" :subtitle="dividend.payment_date">
        <template #append>
          <v-btn icon="mdi-delete" variant="text" size="small" @click="onDelete(dividend.id)" />
        </template>
      </v-list-item>
    </v-list>

    <DividendFormDialog v-model:open="dialogOpen" />
  </v-card>
</template>
