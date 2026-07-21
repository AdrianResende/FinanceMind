export type AssetClass = 'acao' | 'fii' | 'etf' | 'tesouro_direto'

export interface Asset {
  id: string
  ticker: string
  name: string
  asset_class: AssetClass
  currency: string
}

export interface PriceHistoryPoint {
  price_date: string
  close_price: string
}

export interface MarketBenchmarkPoint {
  ref_date: string
  value: string
}
