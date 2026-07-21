<script setup lang="ts">
import { ref } from 'vue'
import { useDebounceFn } from '@vueuse/core'

import MdiIcon from '@/components/common/MdiIcon.vue'
import { useGlossaryStore } from '@/stores/glossary'

const glossaryStore = useGlossaryStore()
const inputValue = ref(glossaryStore.searchQuery)

const search = useDebounceFn((value: string) => {
  glossaryStore.setSearchQuery(value)
}, 300)

function onInput(value: string) {
  inputValue.value = value
  search(value)
}
</script>

<template>
  <n-input
    :value="inputValue"
    size="large"
    clearable
    placeholder="Busque um termo (ex: FII, Tesouro Selic)"
    @update:value="onInput"
  >
    <template #prefix><MdiIcon name="magnify" :size="18" /></template>
  </n-input>
</template>
