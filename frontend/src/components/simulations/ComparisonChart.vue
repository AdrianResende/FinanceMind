<script setup lang="ts">
import { computed } from 'vue'
import type { ApexOptions } from 'apexcharts'

import { ApexChart } from '@/plugins/apexchart'
import type { ComparisonSeries } from '@/types/simulation'

const props = defineProps<{
  series: ComparisonSeries[]
}>()

const hasData = computed(() => props.series.some((s) => s.points.length > 0))

const chartSeries = computed(() =>
  props.series.map((s) => ({
    name: s.label,
    data: s.points.map((p) => ({ x: p.date, y: Number(p.value) })),
  })),
)

const options = computed<ApexOptions>(() => ({
  chart: { type: 'line', toolbar: { show: false } },
  xaxis: { type: 'datetime' },
  yaxis: { labels: { formatter: (val: number) => `${val.toFixed(1)}%` } },
  dataLabels: { enabled: false },
  stroke: { curve: 'smooth', width: 2 },
  colors: ['#0F4C64', '#0E9C8F', '#C77D18', '#2A7DE1', '#7C7C7C'],
  legend: { position: 'top' },
}))
</script>

<template>
  <ApexChart v-if="hasData" type="line" height="320" :options="options" :series="chartSeries" />
  <p v-else class="text-body">Selecione ao menos um ativo ou indexador para comparar.</p>
</template>
