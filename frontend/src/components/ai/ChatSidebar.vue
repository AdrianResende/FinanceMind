<script setup lang="ts">
import { useAiChatStore } from '@/stores/aiChat'

const aiChatStore = useAiChatStore()

async function selectConversation(id: string) {
  await aiChatStore.selectConversation(id)
}

async function createConversation() {
  await aiChatStore.createConversation()
}

async function removeConversation(id: string, event: Event) {
  event.stopPropagation()
  await aiChatStore.deleteConversation(id)
}
</script>

<template>
  <n-card bordered content-style="padding: 16px" class="glass-card sidebar-card">
    <n-button type="primary" block secondary class="mb-4" @click="createConversation">
      <template #icon><MdiIcon name="plus" :size="18" /></template>
      Nova conversa
    </n-button>

    <n-empty v-if="aiChatStore.conversations.length === 0" description="Nenhuma conversa ainda" size="small" />

    <div v-else class="conversation-list">
      <div
        v-for="conversation in aiChatStore.conversations"
        :key="conversation.id"
        class="conversation-item"
        :class="{ 'conversation-item--active': aiChatStore.activeConversation?.id === conversation.id }"
        @click="selectConversation(conversation.id)"
      >
        <MdiIcon name="chat-outline" :size="16" />
        <span class="conversation-item__title">{{ conversation.title }}</span>
        <n-button quaternary circle size="tiny" @click="removeConversation(conversation.id, $event)">
          <template #icon><MdiIcon name="trash-can-outline" :size="14" /></template>
        </n-button>
      </div>
    </div>
  </n-card>
</template>

<style scoped>
.sidebar-card {
  height: 100%;
}

.conversation-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.conversation-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  border-radius: 10px;
  cursor: pointer;
  color: var(--ink-2);
}

.conversation-item:hover {
  background: rgba(15, 76, 100, 0.08);
}

.conversation-item--active {
  background: rgba(15, 76, 100, 0.12);
  color: var(--brand-primary);
  font-weight: 600;
}

.conversation-item__title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 0.875rem;
}
</style>
