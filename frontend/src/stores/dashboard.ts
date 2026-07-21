import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

import { dividendService } from '@/services/dividendService'
import { portfolioService } from '@/services/portfolioService'
import { useAuthStore } from '@/stores/auth'
import {
  demoAllocation,
  demoBenchmarks,
  demoDividends,
  demoPerformance,
  demoTopMovers,
} from '@/stores/demoData'
import type { AllocationItem, BenchmarkSeries, PerformancePoint, TopMoversResponse } from '@/types/dashboard'
import type { Dividend, DividendCreatePayload } from '@/types/dividend'

export type DashboardPeriod = '1m' | '3m' | '6m' | '1a'

const PERIOD_DAYS: Record<DashboardPeriod, number> = {
  '1m': 30,
  '3m': 90,
  '6m': 180,
  '1a': 365,
}

function periodStartDate(period: DashboardPeriod): string {
  const start = new Date()
  start.setDate(start.getDate() - PERIOD_DAYS[period])
  return start.toISOString().slice(0, 10)
}

export const useDashboardStore = defineStore('dashboard', () => {
  const allocation = ref<AllocationItem[]>([])
  const performance = ref<PerformancePoint[]>([])
  const benchmarks = ref<BenchmarkSeries | null>(null)
  const topMovers = ref<TopMoversResponse | null>(null)
  const dividends = ref<Dividend[]>([])
  const period = ref<DashboardPeriod>('3m')
  const loading = ref(false)
  const error = ref('')

  const totalCurrent = computed(() =>
    allocation.value.reduce((sum, item) => sum + Number(item.value), 0),
  )

  async function loadDashboard() {
    const auth = useAuthStore()
    loading.value = true
    error.value = ''
    try {
      if (auth.isDemoMode) {
        allocation.value = demoAllocation
        performance.value = demoPerformance
        benchmarks.value = demoBenchmarks
        topMovers.value = demoTopMovers
        dividends.value = demoDividends
        return
      }

      const params = { start: periodStartDate(period.value) }
      const [allocationData, performanceData, benchmarksData, topMoversData, dividendsData] = await Promise.all([
        portfolioService.getAllocation(),
        portfolioService.getPerformance(params),
        portfolioService.getBenchmarks(params),
        portfolioService.getTopMovers(),
        dividendService.list({ page_size: 100 }),
      ])
      allocation.value = allocationData
      performance.value = performanceData
      benchmarks.value = benchmarksData
      topMovers.value = topMoversData
      dividends.value = dividendsData.items
    } catch {
      error.value = 'Não foi possível carregar o dashboard.'
    } finally {
      loading.value = false
    }
  }

  async function setPeriod(newPeriod: DashboardPeriod) {
    period.value = newPeriod
    await loadDashboard()
  }

  async function createDividend(payload: DividendCreatePayload) {
    const auth = useAuthStore()
    if (auth.isDemoMode) {
      throw new Error('Ação indisponível em modo demonstração.')
    }
    await dividendService.create(payload)
    await loadDashboard()
  }

  async function deleteDividend(id: string) {
    const auth = useAuthStore()
    if (auth.isDemoMode) {
      return
    }
    await dividendService.remove(id)
    await loadDashboard()
  }

  return {
    allocation,
    performance,
    benchmarks,
    topMovers,
    dividends,
    period,
    loading,
    error,
    totalCurrent,
    loadDashboard,
    setPeriod,
    createDividend,
    deleteDividend,
  }
})
