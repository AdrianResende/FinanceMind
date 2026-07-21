<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useDebounceFn } from '@vueuse/core'
import { useRouter } from 'vue-router'

import MdiIcon from '@/components/common/MdiIcon.vue'
import { useMarketStore } from '@/stores/market'

const marketStore = useMarketStore()
const router = useRouter()
const query = ref('')

const CLASS_LABELS: Record<string, string> = {
  acao: 'Ação',
  fii: 'FII',
  etf: 'ETF',
  tesouro_direto: 'Tesouro Direto',
}

const search = useDebounceFn((value: string) => {
  marketStore.search(value)
}, 300)

function onInput(value: string) {
  query.value = value
  search(value)
}

function goToAsset(ticker: string) {
  router.push({ name: 'market-asset-detail', params: { ticker } })
}

onMounted(() => {
  marketStore.search('')
})
</script>

<template>
  <div>
    <n-input
      :value="query"
      size="large"
      clearable
      placeholder="Busque por ticker ou nome (ex: PETR4, Tesouro Selic)"
      @update:value="onInput"
    >
      <template #prefix><MdiIcon name="magnify" :size="18" /></template>
    </n-input>

    <n-list class="mt-6" :show-divider="false">
      <n-list-item
        v-for="asset in marketStore.searchResults"
        :key="asset.id"
        class="asset-row"
        @click="goToAsset(asset.ticker)"
      >
        <div class="asset-row__content">
          <div>
            <div class="text-title" style="font-size: 1rem">{{ asset.ticker }}</div>
            <div class="text-body">{{ asset.name }}</div>
          </div>
          <n-tag round :bordered="false">{{ CLASS_LABELS[asset.asset_class] ?? asset.asset_class }}</n-tag>
        </div>
      </n-list-item>
    </n-list>

    <p v-if="!marketStore.searchLoading && marketStore.searchResults.length === 0" class="text-body mt-4">
      Nenhum ativo encontrado.
    </p>
  </div>
</template>

<style scoped>
.asset-row {
  cursor: pointer;
  border-radius: 12px;
  padding-inline: var(--space-3);
  transition: background 0.15s ease;
}

.asset-row:hover {
  background: rgba(15, 76, 100, 0.06);
}

.asset-row__content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}
</style>
