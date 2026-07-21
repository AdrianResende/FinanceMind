import { api } from '@/services/api'
import type { Asset, MarketBenchmarkPoint, PriceHistoryPoint } from '@/types/asset'

export const assetService = {
  search(q: string) {
    return api.get<Asset[]>('/market/assets', { params: { q } }).then((r) => r.data)
  },
  getDetail(ticker: string) {
    return api.get<Asset>(`/market/assets/${ticker}`).then((r) => r.data)
  },
  getHistory(ticker: string) {
    return api.get<PriceHistoryPoint[]>(`/market/assets/${ticker}/history`).then((r) => r.data)
  },
  getBenchmark(code: string) {
    return api.get<MarketBenchmarkPoint[]>(`/market/benchmarks/${code}`).then((r) => r.data)
  },
}
