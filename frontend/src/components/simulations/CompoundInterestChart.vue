<script setup lang="ts">
import { computed } from 'vue'
import type { ApexOptions } from 'apexcharts'

import { ApexChart } from '@/plugins/apexchart'
import type { CompoundInterestPoint } from '@/types/simulation'

const props = defineProps<{
  points: CompoundInterestPoint[]
}>()

const hasData = computed(() => props.points.length > 0)

const chartSeries = computed(() => [
  { name: 'Total investido', data: props.points.map((p) => ({ x: p.month, y: Number(p.invested) })) },
  { name: 'Total acumulado', data: props.points.map((p) => ({ x: p.month, y: Number(p.total) })) },
])

const options = computed<ApexOptions>(() => ({
  chart: { type: 'area', toolbar: { show: false } },
  xaxis: { title: { text: 'Meses' }, tickAmount: Math.min(props.points.length - 1, 12) },
  yaxis: {
    labels: {
      formatter: (val: number) =>
        val.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 }),
    },
  },
  dataLabels: { enabled: false },
  stroke: { curve: 'smooth', width: 2 },
  fill: { type: 'gradient', gradient: { opacityFrom: 0.35, opacityTo: 0.02 } },
  colors: ['#7C7C7C', '#0E9C8F'],
  legend: { position: 'top' },
}))
</script>

<template>
  <ApexChart v-if="hasData" type="area" height="320" :options="options" :series="chartSeries" />
</template>
