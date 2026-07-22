<script setup lang="ts">
import { nextTick, ref, watch } from 'vue'

import { useAiChatStore } from '@/stores/aiChat'

const aiChatStore = useAiChatStore()
const draft = ref('')
const messagesRef = ref<HTMLDivElement | null>(null)

function scrollToBottom() {
  nextTick(() => {
    if (messagesRef.value) {
      messagesRef.value.scrollTop = messagesRef.value.scrollHeight
    }
  })
}

watch(() => aiChatStore.activeConversation?.messages.length, scrollToBottom)
watch(() => aiChatStore.activeConversation?.id, scrollToBottom)

async function send() {
  const content = draft.value.trim()
  if (!content || aiChatStore.sending) return
  draft.value = ''
  await aiChatStore.sendMessage(content)
}

function onKeydown(event: KeyboardEvent) {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    send()
  }
}

function usagePct() {
  const usage = aiChatStore.usage
  if (!usage || usage.limit === 0) return 0
  return Math.min(100, Math.round((usage.used / usage.limit) * 100))
}
</script>

<template>
  <n-card bordered content-style="padding: 0" class="glass-card chat-card">
    <div v-if="!aiChatStore.activeConversation" class="chat-placeholder">
      <MdiIcon name="robot-outline" :size="40" />
      <p class="text-body">Selecione uma conversa ou crie uma nova para começar.</p>
    </div>

    <template v-else>
      <div class="chat-header">
        <span class="text-title" style="font-size: 1rem">{{ aiChatStore.activeConversation.title }}</span>
        <n-tag v-if="aiChatStore.usage" round :bordered="false" size="small">
          {{ aiChatStore.usage.used }}/{{ aiChatStore.usage.limit }} mensagens este mês
        </n-tag>
      </div>
      <n-progress
        v-if="aiChatStore.usage"
        type="line"
        :percentage="usagePct()"
        :height="3"
        :show-indicator="false"
        :border-radius="0"
      />

      <div ref="messagesRef" class="chat-messages">
        <div
          v-for="message in aiChatStore.activeConversation.messages"
          :key="message.id"
          class="chat-message"
          :class="`chat-message--${message.role}`"
        >
          <div class="chat-bubble">
            {{ message.content }}
          </div>
          <div v-if="message.disclaimer" class="chat-disclaimer">
            <MdiIcon name="information-outline" :size="14" />
            {{ message.disclaimer }}
          </div>
        </div>

        <div v-if="aiChatStore.sending" class="chat-message chat-message--assistant">
          <div class="chat-bubble chat-bubble--typing">
            <span class="typing-dot" />
            <span class="typing-dot" />
            <span class="typing-dot" />
          </div>
        </div>
      </div>

      <n-alert v-if="aiChatStore.error" type="error" :show-icon="false" class="chat-error">
        {{ aiChatStore.error }}
      </n-alert>

      <div class="chat-input">
        <n-input
          v-model:value="draft"
          type="textarea"
          placeholder="Pergunte sobre investimentos, renda fixa, dividendos..."
          :autosize="{ minRows: 1, maxRows: 4 }"
          :disabled="aiChatStore.sending"
          @keydown="onKeydown"
        />
        <n-button type="primary" circle :loading="aiChatStore.sending" :disabled="!draft.trim()" @click="send">
          <template #icon><MdiIcon name="send" :size="18" /></template>
        </n-button>
      </div>
    </template>
  </n-card>
</template>

<style scoped>
.chat-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chat-card :deep(.n-card__content) {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.chat-placeholder {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-3);
  color: var(--ink-3);
  padding: var(--space-8);
}

.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4) var(--space-4) var(--space-3);
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.chat-message {
  display: flex;
  flex-direction: column;
  max-width: 80%;
}

.chat-message--user {
  align-self: flex-end;
  align-items: flex-end;
}

.chat-message--assistant {
  align-self: flex-start;
  align-items: flex-start;
}

.chat-bubble {
  padding: var(--space-3) var(--space-4);
  border-radius: 16px;
  white-space: pre-wrap;
  font-size: 0.9375rem;
  line-height: 1.5;
}

.chat-message--user .chat-bubble {
  background: var(--brand-primary);
  color: #fff;
  border-bottom-right-radius: 4px;
}

.chat-message--assistant .chat-bubble {
  background: rgba(15, 76, 100, 0.08);
  color: var(--ink-1);
  border-bottom-left-radius: 4px;
}

.chat-bubble--typing {
  display: flex;
  gap: 4px;
  align-items: center;
}

.typing-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--ink-3);
  animation: typing-bounce 1.2s infinite ease-in-out;
}

.typing-dot:nth-child(2) {
  animation-delay: 0.15s;
}

.typing-dot:nth-child(3) {
  animation-delay: 0.3s;
}

@keyframes typing-bounce {
  0%,
  60%,
  100% {
    opacity: 0.35;
    transform: translateY(0);
  }
  30% {
    opacity: 1;
    transform: translateY(-3px);
  }
}

.chat-disclaimer {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: var(--space-1);
  font-size: 0.75rem;
  color: var(--ink-3);
  max-width: 90%;
}

.chat-error {
  margin: 0 var(--space-4) var(--space-3);
}

.chat-input {
  display: flex;
  align-items: flex-end;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-4) var(--space-4);
  border-top: 1px solid var(--glass-border);
}

.chat-input :deep(.n-input) {
  flex: 1;
}
</style>
