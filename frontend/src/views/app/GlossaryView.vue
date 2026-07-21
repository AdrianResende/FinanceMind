<script setup lang="ts">
import { onMounted } from 'vue'

import GlossaryCategoryList from '@/components/glossary/GlossaryCategoryList.vue'
import GlossarySearchBar from '@/components/glossary/GlossarySearchBar.vue'
import GlossaryTermCard from '@/components/glossary/GlossaryTermCard.vue'
import GlossaryTermDetail from '@/components/glossary/GlossaryTermDetail.vue'
import { useGlossaryStore } from '@/stores/glossary'

const glossaryStore = useGlossaryStore()

onMounted(async () => {
  await Promise.all([glossaryStore.loadCategories(), glossaryStore.loadTerms()])
})
</script>

<template>
  <div>
    <h1 class="text-section-title mb-6">Aprendizado</h1>

    <div class="mb-6">
      <GlossarySearchBar class="mb-4" />
      <GlossaryCategoryList />
    </div>

    <n-alert v-if="glossaryStore.error" type="error" class="mb-4">{{ glossaryStore.error }}</n-alert>

    <n-grid v-if="glossaryStore.terms.length" :x-gap="20" :y-gap="20" cols="1 s:2 m:3" responsive="screen">
      <n-grid-item v-for="term in glossaryStore.terms" :key="term.slug">
        <GlossaryTermCard :term="term" @select="glossaryStore.openTerm" />
      </n-grid-item>
    </n-grid>
    <p v-else-if="!glossaryStore.loading" class="text-body">Nenhum termo encontrado.</p>

    <GlossaryTermDetail />
  </div>
</template>
