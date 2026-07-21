import { api } from '@/services/api'
import type {
  AssetComparisonRequest,
  AssetComparisonResponse,
  CompoundInterestRequest,
  CompoundInterestResponse,
} from '@/types/simulation'

export const simulationService = {
  compoundInterest(payload: CompoundInterestRequest) {
    return api.post<CompoundInterestResponse>('/simulations/compound-interest', payload).then((r) => r.data)
  },
  compareAssets(payload: AssetComparisonRequest) {
    return api.post<AssetComparisonResponse>('/simulations/compare-assets', payload).then((r) => r.data)
  },
}
