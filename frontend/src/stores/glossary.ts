import { defineStore } from 'pinia'
import { ref } from 'vue'

import { glossaryService } from '@/services/glossaryService'
import { useAuthStore } from '@/stores/auth'
import { demoGlossaryCategories, demoGlossaryTerms } from '@/stores/demoData'
import type { GlossaryCategory, GlossaryTermDetail, GlossaryTermListItem } from '@/types/glossary'

export const useGlossaryStore = defineStore('glossary', () => {
  const categories = ref<GlossaryCategory[]>([])
  const terms = ref<GlossaryTermListItem[]>([])
  const selectedTerm = ref<GlossaryTermDetail | null>(null)
  const activeCategory = ref<string | null>(null)
  const searchQuery = ref('')
  const loading = ref(false)
  const error = ref('')

  async function loadCategories() {
    const auth = useAuthStore()
    categories.value = auth.isDemoMode ? demoGlossaryCategories : await glossaryService.listCategories()
  }

  async function loadTerms() {
    const auth = useAuthStore()
    loading.value = true
    error.value = ''
    try {
      if (auth.isDemoMode) {
        const query = searchQuery.value.trim().toLowerCase()
        terms.value = demoGlossaryTerms.filter((term) => {
          const matchesCategory = !activeCategory.value || term.category.slug === activeCategory.value
          const matchesQuery =
            !query ||
            term.term.toLowerCase().includes(query) ||
            term.short_definition.toLowerCase().includes(query)
          return matchesCategory && matchesQuery
        })
        return
      }
      terms.value = await glossaryService.listTerms({
        category: activeCategory.value ?? undefined,
        q: searchQuery.value || undefined,
      })
    } catch {
      error.value = 'Não foi possível carregar o glossário.'
    } finally {
      loading.value = false
    }
  }

  async function setCategory(slug: string | null) {
    activeCategory.value = slug
    await loadTerms()
  }

  async function setSearchQuery(q: string) {
    searchQuery.value = q
    await loadTerms()
  }

  async function openTerm(slug: string) {
    const auth = useAuthStore()
    if (auth.isDemoMode) {
      selectedTerm.value = demoGlossaryTerms.find((term) => term.slug === slug) ?? null
      return
    }
    selectedTerm.value = await glossaryService.getTerm(slug)
  }

  function closeTerm() {
    selectedTerm.value = null
  }

  return {
    categories,
    terms,
    selectedTerm,
    activeCategory,
    searchQuery,
    loading,
    error,
    loadCategories,
    loadTerms,
    setCategory,
    setSearchQuery,
    openTerm,
    closeTerm,
  }
})
