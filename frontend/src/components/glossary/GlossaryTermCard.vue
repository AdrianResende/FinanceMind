<script setup lang="ts">
import type { GlossaryTermListItem } from '@/types/glossary'

defineProps<{
  term: GlossaryTermListItem
}>()

const emit = defineEmits<{
  select: [slug: string]
}>()
</script>

<template>
  <n-card
    hoverable
    bordered
    content-style="padding: 20px"
    class="glass-card term-card"
    @click="emit('select', term.slug)"
  >
    <n-tag size="small" round :bordered="false" class="mb-2">{{ term.category.name }}</n-tag>
    <div class="text-title" style="font-size: 1.0625rem">{{ term.term }}</div>
    <p class="text-body mt-2">{{ term.short_definition }}</p>
  </n-card>
</template>

<style scoped>
.term-card {
  cursor: pointer;
  height: 100%;
}
</style>
