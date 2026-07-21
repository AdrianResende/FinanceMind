<script setup lang="ts">
withDefaults(
  defineProps<{
    name: string
    size?: number | string
    color?: string
  }>(),
  { size: 20, color: undefined },
)
</script>

<template>
  <i
    :class="`mdi mdi-${name}`"
    :style="{ fontSize: typeof size === 'number' ? `${size}px` : size, color, lineHeight: 1 }"
  />
</template>
