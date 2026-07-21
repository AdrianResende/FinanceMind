import type { Asset } from '@/types/asset'

export type TransactionOperation = 'compra' | 'venda'

export interface Transaction {
  id: string
  asset: Asset
  operation: TransactionOperation
  quantity: string
  unit_price: string
  fees: string
  operation_date: string
}

export interface TransactionCreatePayload {
  asset_id: string
  operation: TransactionOperation
  quantity: string
  unit_price: string
  fees: string
  operation_date: string
}

export type TransactionUpdatePayload = Partial<TransactionCreatePayload>

export interface TransactionListResponse {
  items: Transaction[]
  total: number
  page: number
  page_size: number
}
