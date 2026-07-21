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
  <v-card class="pa-4">
    <v-card-title>Maiores variações</v-card-title>
    <v-row v-if="data && (data.gainers.length || data.losers.length)">
      <v-col cols="12" sm="6">
        <div class="text-caption text-medium-emphasis mb-1">Altas</div>
        <v-list density="compact">
          <v-list-item v-for="item in data.gainers" :key="item.asset.id" :title="item.asset.ticker">
            <template #append>
              <span class="text-success font-weight-medium">{{ formatChange(item.change_pct) }}</span>
            </template>
          </v-list-item>
        </v-list>
      </v-col>
      <v-col cols="12" sm="6">
        <div class="text-caption text-medium-emphasis mb-1">Baixas</div>
        <v-list density="compact">
          <v-list-item v-for="item in data.losers" :key="item.asset.id" :title="item.asset.ticker">
            <template #append>
              <span class="text-error font-weight-medium">{{ formatChange(item.change_pct) }}</span>
            </template>
          </v-list-item>
        </v-list>
      </v-col>
    </v-row>
    <p v-else class="text-body-2 text-medium-emphasis pa-4">
      Ainda não há dados suficientes (é preciso pelo menos 2 dias de cotação por ativo).
    </p>
  </v-card>
</template>
