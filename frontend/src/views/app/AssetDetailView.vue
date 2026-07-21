<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import AssetPriceChart from '@/components/market/AssetPriceChart.vue'
import MdiIcon from '@/components/common/MdiIcon.vue'
import TransactionFormDialog from '@/components/portfolio/TransactionFormDialog.vue'
import { useMarketStore } from '@/stores/market'

const route = useRoute()
const marketStore = useMarketStore()
const dialogOpen = ref(false)

const CLASS_LABELS: Record<string, string> = {
  acao: 'Ação',
  fii: 'FII',
  etf: 'ETF',
  tesouro_direto: 'Tesouro Direto',
}

const ticker = computed(() => String(route.params.ticker))
const latestPrice = computed(() => marketStore.priceHistory.at(-1)?.close_price ?? null)

function formatCurrency(value: string) {
  return Number(value).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

async function load() {
  await marketStore.loadAssetDetail(ticker.value)
}

onMounted(load)
watch(ticker, load)
</script>

<template>
  <div>
    <n-alert v-if="marketStore.error" type="error" class="mb-4">{{ marketStore.error }}</n-alert>

    <template v-if="marketStore.selectedAsset">
      <div class="asset-header mb-6">
        <div>
          <h1 class="text-section-title">{{ marketStore.selectedAsset.ticker }}</h1>
          <p class="text-body">{{ marketStore.selectedAsset.name }}</p>
        </div>
        <n-button type="primary" round @click="dialogOpen = true">
          <template #icon><MdiIcon name="plus" :size="16" /></template>
          Adicionar à carteira
        </n-button>
      </div>

      <n-grid :x-gap="24" :y-gap="24" cols="1 m:2" responsive="screen" class="mb-6">
        <n-grid-item>
          <n-card bordered hoverable content-style="padding: 24px" class="glass-card stat-card">
            <div class="icon-tile"><MdiIcon name="tag-outline" :size="22" /></div>
            <div>
              <div class="text-muted" style="font-size: 0.8125rem">Classe</div>
              <div class="text-title">
                {{ CLASS_LABELS[marketStore.selectedAsset.asset_class] ?? marketStore.selectedAsset.asset_class }}
              </div>
            </div>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card bordered hoverable content-style="padding: 24px" class="glass-card stat-card">
            <div class="icon-tile"><MdiIcon name="currency-usd" :size="22" /></div>
            <div>
              <div class="text-muted" style="font-size: 0.8125rem">Última cotação</div>
              <div class="text-title">{{ latestPrice ? formatCurrency(latestPrice) : '—' }}</div>
            </div>
          </n-card>
        </n-grid-item>
      </n-grid>

      <AssetPriceChart :history="marketStore.priceHistory" />

      <TransactionFormDialog v-model:open="dialogOpen" :preset-asset="marketStore.selectedAsset" />
    </template>

    <n-spin v-else-if="marketStore.detailLoading" size="large" class="mt-8" />
  </div>
</template>

<style scoped>
.asset-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.stat-card :deep(.n-card__content) {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}
</style>
