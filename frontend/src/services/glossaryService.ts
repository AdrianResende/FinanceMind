import { api } from '@/services/api'
import type { GlossaryCategory, GlossaryTermDetail, GlossaryTermListItem } from '@/types/glossary'

export const glossaryService = {
  listCategories() {
    return api.get<GlossaryCategory[]>('/glossary/categories').then((r) => r.data)
  },
  listTerms(params: { category?: string; q?: string } = {}) {
    return api.get<GlossaryTermListItem[]>('/glossary/terms', { params }).then((r) => r.data)
  },
  getTerm(slug: string) {
    return api.get<GlossaryTermDetail>(`/glossary/terms/${slug}`).then((r) => r.data)
  },
}
