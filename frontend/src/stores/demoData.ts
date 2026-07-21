import type { AllocationItem, BenchmarkSeries, PerformancePoint, TopMoversResponse } from '@/types/dashboard'
import type { Dividend } from '@/types/dividend'
import type { PortfolioSummary } from '@/types/portfolio'
import type { Transaction } from '@/types/transaction'

const petr4 = {
  id: 'demo-asset-petr4',
  ticker: 'PETR4',
  name: 'Petrobras PN',
  asset_class: 'acao' as const,
  currency: 'BRL',
}
const hglg11 = {
  id: 'demo-asset-hglg11',
  ticker: 'HGLG11',
  name: 'CSHG Logística FII',
  asset_class: 'fii' as const,
  currency: 'BRL',
}
const bova11 = {
  id: 'demo-asset-bova11',
  ticker: 'BOVA11',
  name: 'iShares Ibovespa ETF',
  asset_class: 'etf' as const,
  currency: 'BRL',
}
const tesouroSelic = {
  id: 'demo-asset-selic2029',
  ticker: 'TESOURO_SELIC_2029',
  name: 'Tesouro Selic 2029',
  asset_class: 'tesouro_direto' as const,
  currency: 'BRL',
}

export const demoPortfolioSummary: PortfolioSummary = {
  positions: [
    {
      asset: petr4,
      quantity: '100',
      avg_price: '32.10',
      invested_value: '3210.00',
      current_price: '38.50',
      current_value: '3850.00',
      profit: '640.00',
      profit_pct: '19.94',
    },
    {
      asset: hglg11,
      quantity: '25',
      avg_price: '170.00',
      invested_value: '4250.00',
      current_price: '165.20',
      current_value: '4130.00',
      profit: '-120.00',
      profit_pct: '-2.82',
    },
    {
      asset: bova11,
      quantity: '40',
      avg_price: '108.00',
      invested_value: '4320.00',
      current_price: '112.40',
      current_value: '4496.00',
      profit: '176.00',
      profit_pct: '4.07',
    },
    {
      asset: tesouroSelic,
      quantity: '10',
      avg_price: '1500.00',
      invested_value: '15000.00',
      current_price: '1523.40',
      current_value: '15234.00',
      profit: '234.00',
      profit_pct: '1.56',
    },
  ],
  total_invested: '26780.00',
  total_current: '27710.00',
  total_profit: '930.00',
  total_profit_pct: '3.47',
}

export const demoTransactions: Transaction[] = [
  {
    id: 'demo-tx-1',
    asset: petr4,
    operation: 'compra',
    quantity: '100',
    unit_price: '32.10',
    fees: '8.50',
    operation_date: '2026-04-12',
  },
  {
    id: 'demo-tx-2',
    asset: hglg11,
    operation: 'compra',
    quantity: '25',
    unit_price: '170.00',
    fees: '3.20',
    operation_date: '2026-05-03',
  },
  {
    id: 'demo-tx-3',
    asset: bova11,
    operation: 'compra',
    quantity: '40',
    unit_price: '108.00',
    fees: '5.00',
    operation_date: '2026-05-20',
  },
  {
    id: 'demo-tx-4',
    asset: tesouroSelic,
    operation: 'compra',
    quantity: '10',
    unit_price: '1500.00',
    fees: '0.00',
    operation_date: '2026-06-01',
  },
]

export const demoAllocation: AllocationItem[] = [
  { asset_class: 'acao', value: '3850.00', percentage: '13.89' },
  { asset_class: 'fii', value: '4130.00', percentage: '14.90' },
  { asset_class: 'etf', value: '4496.00', percentage: '16.22' },
  { asset_class: 'tesouro_direto', value: '15234.00', percentage: '54.98' },
]

export const demoPerformance: PerformancePoint[] = [
  { date: '2026-02-01', value: '24100.00' },
  { date: '2026-03-01', value: '24980.00' },
  { date: '2026-04-01', value: '25610.00' },
  { date: '2026-05-01', value: '26330.00' },
  { date: '2026-06-01', value: '27020.00' },
  { date: '2026-07-01', value: '27710.00' },
]

export const demoBenchmarks: BenchmarkSeries = {
  portfolio: [
    { date: '2026-02-01', value: '0.00' },
    { date: '2026-03-01', value: '3.65' },
    { date: '2026-04-01', value: '6.27' },
    { date: '2026-05-01', value: '9.25' },
    { date: '2026-06-01', value: '12.12' },
    { date: '2026-07-01', value: '14.98' },
  ],
  cdi: [
    { date: '2026-02-01', value: '0.00' },
    { date: '2026-03-01', value: '0.85' },
    { date: '2026-04-01', value: '1.71' },
    { date: '2026-05-01', value: '2.58' },
    { date: '2026-06-01', value: '3.46' },
    { date: '2026-07-01', value: '4.35' },
  ],
  ipca: [
    { date: '2026-02-01', value: '0.00' },
    { date: '2026-03-01', value: '0.42' },
    { date: '2026-04-01', value: '0.85' },
    { date: '2026-05-01', value: '1.28' },
    { date: '2026-06-01', value: '1.71' },
    { date: '2026-07-01', value: '2.15' },
  ],
  ibov: [
    { date: '2026-02-01', value: '0.00' },
    { date: '2026-03-01', value: '2.10' },
    { date: '2026-04-01', value: '1.40' },
    { date: '2026-05-01', value: '4.80' },
    { date: '2026-06-01', value: '6.90' },
    { date: '2026-07-01', value: '8.30' },
  ],
}

export const demoTopMovers: TopMoversResponse = {
  gainers: [
    { asset: bova11, change_pct: '1.83' },
    { asset: petr4, change_pct: '1.21' },
  ],
  losers: [
    { asset: hglg11, change_pct: '-0.92' },
    { asset: tesouroSelic, change_pct: '-0.05' },
  ],
}

export const demoDividends: Dividend[] = [
  { id: 'demo-div-1', asset: petr4, amount: '42.30', payment_date: '2026-03-20' },
  { id: 'demo-div-2', asset: hglg11, amount: '187.50', payment_date: '2026-04-15' },
  { id: 'demo-div-3', asset: petr4, amount: '38.90', payment_date: '2026-04-20' },
  { id: 'demo-div-4', asset: hglg11, amount: '192.00', payment_date: '2026-05-15' },
  { id: 'demo-div-5', asset: hglg11, amount: '196.50', payment_date: '2026-06-15' },
  { id: 'demo-div-6', asset: petr4, amount: '45.10', payment_date: '2026-06-20' },
]
