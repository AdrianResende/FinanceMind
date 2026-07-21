import { api } from '@/services/api'
import type { Asset } from '@/types/asset'

export const assetService = {
  search(q: string) {
    return api.get<Asset[]>('/market/assets', { params: { q } }).then((r) => r.data)
  },
}
