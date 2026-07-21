import { api } from '@/services/api'
import type { AllocationItem, BenchmarkSeries, PerformancePoint, TopMoversResponse } from '@/types/dashboard'
import type { PortfolioSummary } from '@/types/portfolio'

export const portfolioService = {
  getSummary() {
    return api.get<PortfolioSummary>('/portfolio').then((r) => r.data)
  },
  getAllocation() {
    return api.get<AllocationItem[]>('/portfolio/allocation').then((r) => r.data)
  },
  getPerformance(params: { start?: string; end?: string } = {}) {
    return api.get<PerformancePoint[]>('/portfolio/performance', { params }).then((r) => r.data)
  },
  getBenchmarks(params: { start?: string; end?: string } = {}) {
    return api.get<BenchmarkSeries>('/portfolio/benchmarks', { params }).then((r) => r.data)
  },
  getTopMovers() {
    return api.get<TopMoversResponse>('/portfolio/top-movers').then((r) => r.data)
  },
}
