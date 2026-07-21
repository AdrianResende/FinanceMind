<script setup lang="ts">
import { ref } from 'vue'
import { useDebounceFn } from '@vueuse/core'

import { assetService } from '@/services/assetService'
import type { Asset } from '@/types/asset'

const modelValue = defineModel<Asset | null>({ default: null })

const items = ref<Asset[]>([])
const loading = ref(false)

const search = useDebounceFn(async (query: string) => {
  if (!query) {
    items.value = []
    return
  }
  loading.value = true
  try {
    items.value = await assetService.search(query)
  } catch {
    items.value = []
  } finally {
    loading.value = false
  }
}, 300)
</script>

<template>
  <v-autocomplete
    v-model="modelValue"
    :items="items"
    :loading="loading"
    item-title="ticker"
    item-value="id"
    return-object
    label="Ativo"
    placeholder="Busque por ticker ou nome"
    no-filter
    required
    @update:search="search"
  >
    <template #item="{ props: itemProps, item }">
      <v-list-item v-bind="itemProps" :title="item.ticker" :subtitle="item.name" />
    </template>
  </v-autocomplete>
</template>
