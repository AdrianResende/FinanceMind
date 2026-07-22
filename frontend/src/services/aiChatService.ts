import { api } from '@/services/api'
import type { AIConversation, AIConversationDetail, AIMessage, AIUsage } from '@/types/aiChat'

export const aiChatService = {
  listConversations() {
    return api.get<AIConversation[]>('/ai/chat/conversations').then((r) => r.data)
  },
  createConversation() {
    return api.post<AIConversation>('/ai/chat/conversations').then((r) => r.data)
  },
  getConversation(id: string) {
    return api.get<AIConversationDetail>(`/ai/chat/conversations/${id}`).then((r) => r.data)
  },
  deleteConversation(id: string) {
    return api.delete(`/ai/chat/conversations/${id}`)
  },
  sendMessage(conversationId: string, content: string) {
    return api
      .post<AIMessage>(`/ai/chat/conversations/${conversationId}/messages`, { content })
      .then((r) => r.data)
  },
  getUsage() {
    return api.get<AIUsage>('/ai/chat/usage').then((r) => r.data)
  },
}
