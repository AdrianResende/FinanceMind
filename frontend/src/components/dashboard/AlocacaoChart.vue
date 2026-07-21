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
  <n-card title="Alocação por classe" bordered hoverable content-style="padding: 24px" class="glass-card">
    <ApexChart v-if="items.length" type="donut" height="280" :options="options" :series="series" />
    <p v-else class="text-body">Nenhuma posição para exibir ainda.</p>
  </n-card>
</template>
