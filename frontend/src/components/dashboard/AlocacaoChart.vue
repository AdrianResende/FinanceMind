<script setup lang="ts">
import { computed } from 'vue'
import type { ApexOptions } from 'apexcharts'

import { ApexChart } from '@/plugins/apexchart'
import type { AllocationItem } from '@/types/dashboard'

const props = defineProps<{
  items: AllocationItem[]
}>()

const CLASS_LABELS: Record<string, string> = {
  acao: 'Ações',
  fii: 'FIIs',
  etf: 'ETFs',
  tesouro_direto: 'Tesouro Direto',
}

const series = computed(() => props.items.map((item) => Number(item.value)))

const options = computed<ApexOptions>(() => ({
  chart: { type: 'donut' },
  labels: props.items.map((item) => CLASS_LABELS[item.asset_class] ?? item.asset_class),
  legend: { position: 'bottom' },
  dataLabels: {
    formatter: (val: number) => `${val.toFixed(1)}%`,
  },
}))
</script>

<template>
  <v-card class="pa-4">
    <v-card-title>Alocação por classe</v-card-title>
    <ApexChart v-if="items.length" type="donut" height="280" :options="options" :series="series" />
    <p v-else class="text-body-2 text-medium-emphasis pa-4">Nenhuma posição para exibir ainda.</p>
  </v-card>
</template>
