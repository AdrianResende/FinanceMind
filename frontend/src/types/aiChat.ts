export interface AIMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  created_at: string
  disclaimer: string | null
}

export interface AIConversation {
  id: string
  title: string
  created_at: string
}

export interface AIConversationDetail extends AIConversation {
  messages: AIMessage[]
}

export interface AIUsage {
  plan: 'free' | 'premium'
  used: number
  limit: number
}
