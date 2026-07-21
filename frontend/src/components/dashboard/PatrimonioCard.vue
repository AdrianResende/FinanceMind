<script setup lang="ts">
import { computed } from 'vue'

import type { PerformancePoint } from '@/types/dashboard'

const props = defineProps<{
  total: number
  performance: PerformancePoint[]
}>()

function formatCurrency(value: number) {
  return value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

const dayChange = computed(() => {
  const count = props.performance.length
  if (count < 2) return null
  const previous = props.performance[count - 2]!
  const latest = props.performance[count - 1]!
  const previousValue = Number(previous.value)
  if (previousValue === 0) return null
  return ((Number(latest.value) - previousValue) / previousValue) * 100
})

const tone = computed<'success' | 'error' | undefined>(() => {
  if (dayChange.value === null) return undefined
  return dayChange.value >= 0 ? 'success' : 'error'
})
</script>

<template>
  <v-card class="pa-4 d-flex align-center ga-3">
    <v-avatar color="primary" variant="tonal" icon="mdi-wallet-outline" />
    <div>
      <div class="text-caption text-medium-emphasis">Patrimônio total</div>
      <div class="text-h6">{{ formatCurrency(total) }}</div>
      <div v-if="dayChange !== null" class="text-body-2" :class="tone ? `text-${tone}` : ''">
        {{ dayChange >= 0 ? '+' : '' }}{{ dayChange.toFixed(2) }}% no período
      </div>
    </div>
  </v-card>
</template>
