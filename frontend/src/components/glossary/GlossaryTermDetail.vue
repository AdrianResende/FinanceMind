<script setup lang="ts">
import { useGlossaryStore } from '@/stores/glossary'

const glossaryStore = useGlossaryStore()

function close() {
  glossaryStore.closeTerm()
}
</script>

<template>
  <n-modal :show="glossaryStore.selectedTerm !== null" @update:show="close">
    <n-card
      v-if="glossaryStore.selectedTerm"
      style="width: 520px"
      :bordered="false"
      size="huge"
      role="dialog"
      aria-modal="true"
      class="glass-card glass-card--strong"
      closable
      @close="close"
    >
      <n-tag size="small" round :bordered="false" class="mb-2">
        {{ glossaryStore.selectedTerm.category.name }}
      </n-tag>
      <h2 class="text-title mb-4">{{ glossaryStore.selectedTerm.term }}</h2>
      <p class="text-body mb-4">{{ glossaryStore.selectedTerm.full_explanation }}</p>
      <n-alert v-if="glossaryStore.selectedTerm.example" type="info" :bordered="false">
        <strong>Exemplo:</strong> {{ glossaryStore.selectedTerm.example }}
      </n-alert>
    </n-card>
  </n-modal>
</template>
