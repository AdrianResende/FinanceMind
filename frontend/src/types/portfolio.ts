import type { Asset } from '@/types/asset'

export interface PositionItem {
  asset: Asset
  quantity: string
  avg_price: string
  invested_value: string
  current_price: string
  current_value: string
  profit: string
  profit_pct: string
}

export interface PortfolioSummary {
  positions: PositionItem[]
  total_invested: string
  total_current: string
  total_profit: string
  total_profit_pct: string
}
