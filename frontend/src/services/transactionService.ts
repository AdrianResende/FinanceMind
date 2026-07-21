import { api } from '@/services/api'
import type {
  TransactionCreatePayload,
  TransactionListResponse,
  TransactionUpdatePayload,
} from '@/types/transaction'

export const transactionService = {
  list(params: { asset_id?: string; page?: number; page_size?: number } = {}) {
    return api.get<TransactionListResponse>('/transactions', { params }).then((r) => r.data)
  },
  create(payload: TransactionCreatePayload) {
    return api.post('/transactions', payload).then((r) => r.data)
  },
  update(id: string, payload: TransactionUpdatePayload) {
    return api.patch(`/transactions/${id}`, payload).then((r) => r.data)
  },
  remove(id: string) {
    return api.delete(`/transactions/${id}`)
  },
}
