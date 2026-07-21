import type { Asset } from '@/types/asset'

export interface Dividend {
  id: string
  asset: Asset
  amount: string
  payment_date: string
}

export interface DividendCreatePayload {
  asset_id: string
  amount: string
  payment_date: string
}

export interface DividendListResponse {
  items: Dividend[]
  total: number
  page: number
  page_size: number
}
