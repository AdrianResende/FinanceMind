<script setup lang="ts">
import type { TopMoversResponse } from '@/types/dashboard'

defineProps<{
  data: TopMoversResponse | null
}>()

function formatChange(value: string) {
  const n = Number(value)
  return `${n >= 0 ? '+' : ''}${n.toFixed(2)}%`
}
</script>

<template>
  <n-card title="Maiores variações" bordered hoverable content-style="padding: 24px" class="glass-card">
    <n-grid v-if="data && (data.gainers.length || data.losers.length)" :x-gap="16" cols="2">
      <n-grid-item>
        <div class="text-muted mover-label">Altas</div>
        <div v-for="item in data.gainers" :key="item.asset.id" class="mover-row">
          <span class="text-body text-truncate">{{ item.asset.ticker }}</span>
          <span class="mover-change" style="color: var(--brand-success)">
            {{ formatChange(item.change_pct) }}
          </span>
        </div>
      </n-grid-item>
      <n-grid-item>
        <div class="text-muted mover-label">Baixas</div>
        <div v-for="item in data.losers" :key="item.asset.id" class="mover-row">
          <span class="text-body text-truncate">{{ item.asset.ticker }}</span>
          <span class="mover-change" style="color: var(--brand-error)">
            {{ formatChange(item.change_pct) }}
          </span>
        </div>
      </n-grid-item>
    </n-grid>
    <p v-else class="text-body">
      Ainda não há dados suficientes (é preciso pelo menos 2 dias de cotação por ativo).
    </p>
  </n-card>
</template>

<style scoped>
.mover-label {
  font-size: 0.8125rem;
  margin-bottom: var(--space-2);
}

.mover-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-2);
  padding-block: var(--space-2);
}

.text-truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.mover-change {
  font-weight: 500;
  flex-shrink: 0;
}
</style>
