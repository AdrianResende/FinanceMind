import { defineStore } from 'pinia'
import { ref } from 'vue'

import { portfolioService } from '@/services/portfolioService'
import { transactionService } from '@/services/transactionService'
import { useAuthStore } from '@/stores/auth'
import { demoPortfolioSummary, demoTransactions } from '@/stores/demoData'
import type { PortfolioSummary } from '@/types/portfolio'
import type { Transaction, TransactionCreatePayload, TransactionUpdatePayload } from '@/types/transaction'

export const usePortfolioStore = defineStore('portfolio', () => {
  const summary = ref<PortfolioSummary | null>(null)
  const transactions = ref<Transaction[]>([])
  const loading = ref(false)
  const error = ref('')

  async function fetchSummary() {
    const auth = useAuthStore()
    summary.value = auth.isDemoMode ? demoPortfolioSummary : await portfolioService.getSummary()
  }

  async function fetchTransactions() {
    const auth = useAuthStore()
    if (auth.isDemoMode) {
      transactions.value = demoTransactions
      return
    }
    const data = await transactionService.list({ page_size: 100 })
    transactions.value = data.items
  }

  async function loadAll() {
    loading.value = true
    error.value = ''
    try {
      await Promise.all([fetchSummary(), fetchTransactions()])
    } catch {
      error.value = 'Não foi possível carregar sua carteira.'
    } finally {
      loading.value = false
    }
  }

  async function createTransaction(payload: TransactionCreatePayload) {
    const auth = useAuthStore()
    if (auth.isDemoMode) {
      throw new Error('Ação indisponível em modo demonstração.')
    }
    await transactionService.create(payload)
    await loadAll()
  }

  async function updateTransaction(id: string, payload: TransactionUpdatePayload) {
    const auth = useAuthStore()
    if (auth.isDemoMode) {
      throw new Error('Ação indisponível em modo demonstração.')
    }
    await transactionService.update(id, payload)
    await loadAll()
  }

  async function deleteTransaction(id: string) {
    const auth = useAuthStore()
    if (auth.isDemoMode) {
      return
    }
    await transactionService.remove(id)
    await loadAll()
  }

  return {
    summary,
    transactions,
    loading,
    error,
    loadAll,
    fetchSummary,
    fetchTransactions,
    createTransaction,
    updateTransaction,
    deleteTransaction,
  }
})
