import { defineStore } from 'pinia'
import { ref } from 'vue'

import { simulationService } from '@/services/simulationService'
import { useAuthStore } from '@/stores/auth'
import { demoComparisonSeries } from '@/stores/demoData'
import type {
  AssetComparisonRequest,
  AssetComparisonResponse,
  CompoundInterestRequest,
  CompoundInterestResponse,
} from '@/types/simulation'

function computeCompoundInterestLocally(payload: CompoundInterestRequest): CompoundInterestResponse {
  const initial = Number(payload.initial_amount)
  const monthly = Number(payload.monthly_amount)
  const annualRate = Number(payload.annual_rate_pct) / 100
  const monthlyRate = (1 + annualRate) ** (1 / 12) - 1

  let balance = initial
  let invested = initial
  const points = [{ month: 0, invested, total: balance, interest: balance - invested }]

  for (let month = 1; month <= payload.months; month += 1) {
    balance = balance * (1 + monthlyRate) + monthly
    invested += monthly
    points.push({ month, invested, total: balance, interest: balance - invested })
  }

  return {
    points: points.map((p) => ({
      month: p.month,
      invested: p.invested.toFixed(2),
      total: p.total.toFixed(2),
      interest: p.interest.toFixed(2),
    })),
    total_invested: invested.toFixed(2),
    total_interest: (balance - invested).toFixed(2),
    final_amount: balance.toFixed(2),
  }
}

export const useSimulationStore = defineStore('simulation', () => {
  const compoundInterestResult = ref<CompoundInterestResponse | null>(null)
  const comparisonResult = ref<AssetComparisonResponse | null>(null)
  const loading = ref(false)
  const error = ref('')

  async function runCompoundInterest(payload: CompoundInterestRequest) {
    const auth = useAuthStore()
    loading.value = true
    error.value = ''
    try {
      compoundInterestResult.value = auth.isDemoMode
        ? computeCompoundInterestLocally(payload)
        : await simulationService.compoundInterest(payload)
    } catch {
      error.value = 'Não foi possível calcular a simulação.'
    } finally {
      loading.value = false
    }
  }

  async function runComparison(payload: AssetComparisonRequest) {
    const auth = useAuthStore()
    loading.value = true
    error.value = ''
    try {
      if (auth.isDemoMode) {
        const wantedKeys = new Set([...payload.tickers, ...payload.benchmark_codes])
        comparisonResult.value = {
          series: demoComparisonSeries.filter((series) => wantedKeys.has(series.key)),
        }
        return
      }
      comparisonResult.value = await simulationService.compareAssets(payload)
    } catch {
      error.value = 'Não foi possível comparar os ativos selecionados.'
    } finally {
      loading.value = false
    }
  }

  return {
    compoundInterestResult,
    comparisonResult,
    loading,
    error,
    runCompoundInterest,
    runComparison,
  }
})
