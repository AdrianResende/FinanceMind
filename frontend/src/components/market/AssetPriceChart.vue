<script setup lang="ts">
import { computed } from 'vue'
import type { ApexOptions } from 'apexcharts'

import { ApexChart } from '@/plugins/apexchart'
import type { PriceHistoryPoint } from '@/types/asset'

const props = defineProps<{
  history: PriceHistoryPoint[]
}>()

const hasData = computed(() => props.history.length > 0)

const chartSeries = computed(() => [
  {
    name: 'Preço de fechamento',
    data: props.history.map((point) => ({ x: point.price_date, y: Number(point.close_price) })),
  },
])

const options = computed<ApexOptions>(() => ({
  chart: { type: 'area', toolbar: { show: false } },
  xaxis: { type: 'datetime' },
  yaxis: {
    labels: {
      formatter: (val: number) =>
        val.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }),
    },
  },
  dataLabels: { enabled: false },
  stroke: { curve: 'smooth', width: 2 },
  fill: { type: 'gradient', gradient: { opacityFrom: 0.35, opacityTo: 0.02 } },
  colors: ['#0F4C64'],
}))
</script>

<template>
  <n-card title="Histórico de preço" bordered hoverable content-style="padding: 24px" class="glass-card">
    <ApexChart v-if="hasData" type="area" height="300" :options="options" :series="chartSeries" />
    <p v-else class="text-body">Ainda não há histórico de preços suficiente para este ativo.</p>
  </n-card>
</template>
