import type { Asset } from '@/types/asset'

export interface AllocationItem {
  asset_class: string
  value: string
  percentage: string
}

export interface PerformancePoint {
  date: string
  value: string
}

export interface BenchmarkPoint {
  date: string
  value: string
}

export interface BenchmarkSeries {
  portfolio: BenchmarkPoint[]
  cdi: BenchmarkPoint[]
  ipca: BenchmarkPoint[]
  ibov: BenchmarkPoint[]
}

export interface TopMoverItem {
  asset: Asset
  change_pct: string
}

export interface TopMoversResponse {
  gainers: TopMoverItem[]
  losers: TopMoverItem[]
}
