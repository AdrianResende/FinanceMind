<script setup lang="ts">
import { onMounted } from 'vue'

import ChatSidebar from '@/components/ai/ChatSidebar.vue'
import ChatWindow from '@/components/ai/ChatWindow.vue'
import { useAiChatStore } from '@/stores/aiChat'

const aiChatStore = useAiChatStore()

onMounted(async () => {
  await Promise.all([aiChatStore.loadConversations(), aiChatStore.loadUsage()])
  if (!aiChatStore.activeConversation && aiChatStore.conversations.length > 0) {
    await aiChatStore.selectConversation(aiChatStore.conversations[0]!.id)
  }
})
</script>

<template>
  <div class="ia-view">
    <h1 class="text-section-title mb-6">IA</h1>
    <n-grid :x-gap="24" cols="1 m:4" responsive="screen" class="ia-grid">
      <n-grid-item span="1">
        <ChatSidebar />
      </n-grid-item>
      <n-grid-item span="1 m:3">
        <ChatWindow />
      </n-grid-item>
    </n-grid>
  </div>
</template>

<style scoped>
.ia-view {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 64px - var(--space-6) * 2);
}

.ia-grid {
  flex: 1;
  min-height: 0;
}

.ia-grid :deep(.n-grid-item) {
  height: 100%;
}
</style>
