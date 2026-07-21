<script setup lang="ts">
import AssetComparisonSimulator from '@/components/simulations/AssetComparisonSimulator.vue'
import CompoundInterestSimulator from '@/components/simulations/CompoundInterestSimulator.vue'
</script>

<template>
  <div>
    <h1 class="text-section-title mb-6">Simulações</h1>

    <n-tabs type="line" animated default-value="juros-compostos">
      <n-tab-pane name="juros-compostos" tab="Juros compostos">
        <CompoundInterestSimulator />
      </n-tab-pane>
      <n-tab-pane name="comparacao" tab="Comparação de ativos">
        <AssetComparisonSimulator />
      </n-tab-pane>
    </n-tabs>
  </div>
</template>
