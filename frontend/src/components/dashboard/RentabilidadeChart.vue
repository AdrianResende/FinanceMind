<script setup lang="ts">
import { computed } from 'vue'
import type { ApexOptions } from 'apexcharts'

import { ApexChart } from '@/plugins/apexchart'
import type { BenchmarkPoint, BenchmarkSeries } from '@/types/dashboard'

const props = defineProps<{
  series: BenchmarkSeries | null
}>()

function toSeriesData(points: BenchmarkPoint[]) {
  return points.map((p) => ({ x: p.date, y: Number(p.value) }))
}

const hasData = computed(() => (props.series?.portfolio.length ?? 0) > 0)

const chartSeries = computed(() => {
  if (!props.series) return []
  return [
    { name: 'Carteira', data: toSeriesData(props.series.portfolio) },
    { name: 'CDI', data: toSeriesData(props.series.cdi) },
    { name: 'IPCA', data: toSeriesData(props.series.ipca) },
    { name: 'IBOV', data: toSeriesData(props.series.ibov) },
  ]
})

const options = computed<ApexOptions>(() => ({
  chart: { type: 'line', toolbar: { show: false } },
  xaxis: { type: 'datetime' },
  yaxis: { labels: { formatter: (val: number) => `${val.toFixed(1)}%` } },
  dataLabels: { enabled: false },
  stroke: { curve: 'smooth', width: 2 },
  colors: ['#0F4C64', '#0E9C8F', '#C77D18', '#7C7C7C'],
}))
</script>

<template>
  <v-card class="pa-4">
    <v-card-title>Rentabilidade vs. benchmarks</v-card-title>
    <ApexChart v-if="hasData" type="line" height="300" :options="options" :series="chartSeries" />
    <p v-else class="text-body-2 text-medium-emphasis pa-4">
      Ainda não há histórico suficiente para comparar com CDI/IPCA/IBOV.
    </p>
  </v-card>
</template>
