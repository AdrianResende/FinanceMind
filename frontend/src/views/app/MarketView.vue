<script setup lang="ts">
import AssetSearchBar from '@/components/market/AssetSearchBar.vue'
</script>

<template>
  <div>
    <h1 class="text-section-title mb-6">Mercado</h1>
    <n-card bordered content-style="padding: 24px" class="glass-card">
      <AssetSearchBar />
    </n-card>
  </div>
</template>
