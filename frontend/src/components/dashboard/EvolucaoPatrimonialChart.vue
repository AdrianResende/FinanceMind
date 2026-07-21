<script setup lang="ts">
import { computed } from 'vue'
import type { ApexOptions } from 'apexcharts'

import { ApexChart } from '@/plugins/apexchart'
import type { PerformancePoint } from '@/types/dashboard'

const props = defineProps<{
  points: PerformancePoint[]
}>()

const series = computed(() => [
  {
    name: 'Patrimônio',
    data: props.points.map((p) => ({ x: p.date, y: Number(p.value) })),
  },
])

const options = computed<ApexOptions>(() => ({
  chart: { type: 'area', toolbar: { show: false } },
  xaxis: { type: 'datetime' },
  yaxis: { labels: { formatter: (val: number) => val.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 }) } },
  dataLabels: { enabled: false },
  stroke: { curve: 'smooth' },
  colors: ['#0F4C64'],
}))
</script>

<template>
  <n-card
    title="Evolução do patrimônio"
    bordered
    hoverable
    content-style="padding: 24px"
    class="glass-card"
  >
    <ApexChart v-if="points.length" type="area" height="280" :options="options" :series="series" />
    <p v-else class="text-body">Ainda não há histórico de preços suficiente para este gráfico.</p>
  </n-card>
</template>
