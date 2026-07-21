import { defineStore } from 'pinia'
import { ref } from 'vue'

import { assetService } from '@/services/assetService'
import { useAuthStore } from '@/stores/auth'
import { demoAssetPriceHistory, demoAssets, demoMarketBenchmarks } from '@/stores/demoData'
import type { Asset, MarketBenchmarkPoint, PriceHistoryPoint } from '@/types/asset'

export const useMarketStore = defineStore('market', () => {
  const searchResults = ref<Asset[]>([])
  const searchLoading = ref(false)

  const selectedAsset = ref<Asset | null>(null)
  const priceHistory = ref<PriceHistoryPoint[]>([])
  const detailLoading = ref(false)
  const error = ref('')

  async function search(q: string) {
    const auth = useAuthStore()
    searchLoading.value = true
    try {
      if (auth.isDemoMode) {
        const query = q.trim().toUpperCase()
        searchResults.value = query
          ? demoAssets.filter((a) => a.ticker.includes(query) || a.name.toUpperCase().includes(query))
          : demoAssets
        return
      }
      searchResults.value = await assetService.search(q)
    } finally {
      searchLoading.value = false
    }
  }

  async function loadAssetDetail(ticker: string) {
    const auth = useAuthStore()
    detailLoading.value = true
    error.value = ''
    try {
      if (auth.isDemoMode) {
        const asset = demoAssets.find((a) => a.ticker === ticker.toUpperCase())
        if (!asset) {
          error.value = 'Ativo não encontrado.'
          selectedAsset.value = null
          priceHistory.value = []
          return
        }
        selectedAsset.value = asset
        priceHistory.value = demoAssetPriceHistory[asset.ticker] ?? []
        return
      }

      const [asset, history] = await Promise.all([
        assetService.getDetail(ticker),
        assetService.getHistory(ticker),
      ])
      selectedAsset.value = asset
      priceHistory.value = history
    } catch {
      error.value = 'Não foi possível carregar os dados do ativo.'
      selectedAsset.value = null
      priceHistory.value = []
    } finally {
      detailLoading.value = false
    }
  }

  async function getBenchmarkHistory(code: string): Promise<MarketBenchmarkPoint[]> {
    const auth = useAuthStore()
    if (auth.isDemoMode) {
      return demoMarketBenchmarks[code] ?? []
    }
    return assetService.getBenchmark(code)
  }

  return {
    searchResults,
    searchLoading,
    selectedAsset,
    priceHistory,
    detailLoading,
    error,
    search,
    loadAssetDetail,
    getBenchmarkHistory,
  }
})
