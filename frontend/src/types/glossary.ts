export interface GlossaryCategory {
  id: string
  slug: string
  name: string
}

export interface GlossaryTermListItem {
  slug: string
  term: string
  short_definition: string
  category: GlossaryCategory
}

export interface GlossaryTermDetail extends GlossaryTermListItem {
  full_explanation: string
  example: string | null
}
