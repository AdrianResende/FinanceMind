import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

import { aiChatService } from '@/services/aiChatService'
import { useAuthStore } from '@/stores/auth'
import { DEMO_AI_DISCLAIMER, buildDemoAiReply, demoAiConversations } from '@/stores/demoData'
import type { AIConversation, AIConversationDetail, AIUsage } from '@/types/aiChat'

function cloneDemoConversations(): AIConversationDetail[] {
  return demoAiConversations.map((conversation) => ({
    ...conversation,
    messages: conversation.messages.map((message) => ({ ...message })),
  }))
}

function countDemoUsage(conversations: AIConversationDetail[]): number {
  return conversations.reduce(
    (total, conversation) => total + conversation.messages.filter((m) => m.role === 'user').length,
    0,
  )
}

export const useAiChatStore = defineStore('aiChat', () => {
  const demoConversations = ref<AIConversationDetail[]>(cloneDemoConversations())

  const conversations = ref<AIConversation[]>([])
  const activeConversation = ref<AIConversationDetail | null>(null)
  const usage = ref<AIUsage | null>(null)
  const loading = ref(false)
  const sending = ref(false)
  const error = ref('')

  async function loadConversations() {
    const auth = useAuthStore()
    loading.value = true
    error.value = ''
    try {
      conversations.value = auth.isDemoMode
        ? demoConversations.value.map(({ id, title, created_at }) => ({ id, title, created_at }))
        : await aiChatService.listConversations()
    } catch {
      error.value = 'Não foi possível carregar suas conversas.'
    } finally {
      loading.value = false
    }
  }

  async function loadUsage() {
    const auth = useAuthStore()
    if (auth.isDemoMode) {
      usage.value = { plan: 'premium', used: countDemoUsage(demoConversations.value), limit: 1000 }
      return
    }
    try {
      usage.value = await aiChatService.getUsage()
    } catch {
      usage.value = null
    }
  }

  async function selectConversation(id: string) {
    const auth = useAuthStore()
    loading.value = true
    error.value = ''
    try {
      if (auth.isDemoMode) {
        activeConversation.value = demoConversations.value.find((c) => c.id === id) ?? null
        return
      }
      activeConversation.value = await aiChatService.getConversation(id)
    } catch {
      error.value = 'Não foi possível carregar a conversa.'
    } finally {
      loading.value = false
    }
  }

  async function createConversation() {
    const auth = useAuthStore()
    if (auth.isDemoMode) {
      const conversation: AIConversationDetail = {
        id: `demo-conversation-${Date.now()}`,
        title: 'Nova conversa',
        created_at: new Date().toISOString(),
        messages: [],
      }
      demoConversations.value.unshift(conversation)
      await loadConversations()
      activeConversation.value = conversation
      return conversation
    }
    const conversation = await aiChatService.createConversation()
    await loadConversations()
    activeConversation.value = { ...conversation, messages: [] }
    return conversation
  }

  async function deleteConversation(id: string) {
    const auth = useAuthStore()
    if (auth.isDemoMode) {
      demoConversations.value = demoConversations.value.filter((c) => c.id !== id)
    } else {
      await aiChatService.deleteConversation(id)
    }
    if (activeConversation.value?.id === id) {
      activeConversation.value = null
    }
    await loadConversations()
  }

  async function sendMessage(content: string) {
    const auth = useAuthStore()
    if (!activeConversation.value) return

    sending.value = true
    error.value = ''
    try {
      if (auth.isDemoMode) {
        const conversation = activeConversation.value
        conversation.messages.push({
          id: `demo-msg-${Date.now()}`,
          role: 'user',
          content,
          created_at: new Date().toISOString(),
          disclaimer: null,
        })
        if (conversation.title === 'Nova conversa') {
          conversation.title = content.slice(0, 80)
        }
        await new Promise((resolve) => setTimeout(resolve, 500))
        conversation.messages.push({
          id: `demo-msg-${Date.now() + 1}`,
          role: 'assistant',
          content: buildDemoAiReply(content),
          created_at: new Date().toISOString(),
          disclaimer: DEMO_AI_DISCLAIMER,
        })
        await loadUsage()
        return
      }

      activeConversation.value.messages.push({
        id: `pending-${Date.now()}`,
        role: 'user',
        content,
        created_at: new Date().toISOString(),
        disclaimer: null,
      })
      const reply = await aiChatService.sendMessage(activeConversation.value.id, content)
      activeConversation.value.messages.push(reply)
      await loadUsage()
    } catch (err) {
      activeConversation.value.messages.pop()
      error.value =
        axios.isAxiosError(err) && err.response?.status === 429
          ? 'Você atingiu o limite de mensagens de IA do seu plano neste mês.'
          : 'Não foi possível enviar sua mensagem. Tente novamente.'
    } finally {
      sending.value = false
    }
  }

  return {
    conversations,
    activeConversation,
    usage,
    loading,
    sending,
    error,
    loadConversations,
    loadUsage,
    selectConversation,
    createConversation,
    deleteConversation,
    sendMessage,
  }
})
