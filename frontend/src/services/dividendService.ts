import { api } from '@/services/api'
import type { DividendCreatePayload, DividendListResponse } from '@/types/dividend'

export const dividendService = {
  list(params: { page?: number; page_size?: number } = {}) {
    return api.get<DividendListResponse>('/portfolio/dividends', { params }).then((r) => r.data)
  },
  create(payload: DividendCreatePayload) {
    return api.post('/portfolio/dividends', payload).then((r) => r.data)
  },
  remove(id: string) {
    return api.delete(`/portfolio/dividends/${id}`)
  },
}
