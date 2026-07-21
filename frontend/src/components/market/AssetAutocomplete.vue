<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useDebounceFn } from '@vueuse/core'
import type { SelectOption } from 'naive-ui'

import { assetService } from '@/services/assetService'
import type { Asset } from '@/types/asset'

const modelValue = defineModel<Asset | null>({ default: null })

const items = ref<Asset[]>([])
const loading = ref(false)
const selectedId = ref<string | null>(modelValue.value?.id ?? null)

const options = computed<SelectOption[]>(() =>
  items.value.map((asset) => ({
    label: `${asset.ticker} · ${asset.name}`,
    value: asset.id,
  })),
)

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

watch(selectedId, (id) => {
  modelValue.value = items.value.find((asset) => asset.id === id) ?? null
})

watch(
  () => modelValue.value,
  (asset) => {
    if (!asset) {
      selectedId.value = null
      return
    }
    if (!items.value.some((item) => item.id === asset.id)) {
      items.value = [asset, ...items.value]
    }
    selectedId.value = asset.id
  },
  { immediate: true },
)
</script>

<template>
  <n-select
    v-model:value="selectedId"
    filterable
    remote
    clearable
    size="large"
    placeholder="Busque por ticker ou nome"
    :options="options"
    :loading="loading"
    @search="search"
  />
</template>
