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
  <n-card bordered hoverable content-style="padding: 24px" class="glass-card stat-card">
    <div class="icon-tile">
      <MdiIcon name="wallet-outline" :size="22" />
    </div>
    <div>
      <div class="text-muted" style="font-size: 0.8125rem">Patrimônio total</div>
      <div class="text-title">{{ formatCurrency(total) }}</div>
      <div
        v-if="dayChange !== null"
        class="text-body"
        :class="tone === 'success' ? 'text-success' : tone === 'error' ? 'text-error' : ''"
      >
        {{ dayChange >= 0 ? '+' : '' }}{{ dayChange.toFixed(2) }}% no período
      </div>
    </div>
  </n-card>
</template>

<style scoped>
.stat-card :deep(.n-card__content) {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.text-success {
  color: var(--brand-success);
}

.text-error {
  color: var(--brand-error);
}
</style>
