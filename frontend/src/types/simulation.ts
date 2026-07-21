export interface CompoundInterestRequest {
  initial_amount: string
  monthly_amount: string
  annual_rate_pct: string
  months: number
}

export interface CompoundInterestPoint {
  month: number
  invested: string
  total: string
  interest: string
}

export interface CompoundInterestResponse {
  points: CompoundInterestPoint[]
  total_invested: string
  total_interest: string
  final_amount: string
}

export interface AssetComparisonRequest {
  tickers: string[]
  benchmark_codes: string[]
  start: string
  end?: string | null
}

export interface ComparisonPoint {
  date: string
  value: string
}

export interface ComparisonSeries {
  key: string
  label: string
  points: ComparisonPoint[]
}

export interface AssetComparisonResponse {
  series: ComparisonSeries[]
}
