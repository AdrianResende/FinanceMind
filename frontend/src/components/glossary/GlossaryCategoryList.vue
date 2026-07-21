<script setup lang="ts">
import { useGlossaryStore } from '@/stores/glossary'

const glossaryStore = useGlossaryStore()

function select(slug: string | null) {
  glossaryStore.setCategory(slug)
}
</script>

<template>
  <div class="category-chips">
    <n-tag
      round
      :bordered="false"
      :type="glossaryStore.activeCategory === null ? 'primary' : 'default'"
      class="category-chip"
      @click="select(null)"
    >
      Todos
    </n-tag>
    <n-tag
      v-for="category in glossaryStore.categories"
      :key="category.id"
      round
      :bordered="false"
      :type="glossaryStore.activeCategory === category.slug ? 'primary' : 'default'"
      class="category-chip"
      @click="select(category.slug)"
    >
      {{ category.name }}
    </n-tag>
  </div>
</template>

<style scoped>
.category-chips {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.category-chip {
  cursor: pointer;
}
</style>
