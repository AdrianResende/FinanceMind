<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

import AssetAutocomplete from '@/components/market/AssetAutocomplete.vue'
import ComparisonChart from '@/components/simulations/ComparisonChart.vue'
import { useSimulationStore } from '@/stores/simulation'
import type { Asset } from '@/types/asset'

const simulationStore = useSimulationStore()

const assetSlots = ref<(Asset | null)[]>([null, null, null])
const benchmarkCodes = ref<string[]>(['cdi'])
const startDate = ref<string | null>(defaultStartDate())
const endDate = ref<string | null>(null)

const benchmarkOptions = [
  { label: 'CDI', value: 'cdi' },
  { label: 'IPCA', value: 'ipca' },
  { label: 'IBOV', value: 'ibov' },
]

function defaultStartDate() {
  const date = new Date()
  date.setFullYear(date.getFullYear() - 1)
  return date.toISOString().slice(0, 10)
}

const tickers = computed(() => assetSlots.value.filter((a): a is Asset => a !== null).map((a) => a.ticker))

async function simulate() {
  if (!startDate.value) return
  await simulationStore.runComparison({
    tickers: tickers.value,
    benchmark_codes: benchmarkCodes.value,
    start: startDate.value,
    end: endDate.value,
  })
}

onMounted(simulate)
</script>

<template>
  <n-grid :x-gap="24" :y-gap="24" cols="1 m:3" responsive="screen">
    <n-grid-item>
      <n-card title="Parâmetros" bordered content-style="padding: 24px" class="glass-card">
        <n-form label-placement="top">
          <n-form-item v-for="(_, index) in assetSlots" :key="index" :label="`Ativo ${index + 1}`">
            <AssetAutocomplete v-model="assetSlots[index]" style="width: 100%" @update:model-value="simulate" />
          </n-form-item>
          <n-form-item label="Indexadores">
            <n-checkbox-group v-model:value="benchmarkCodes" @update:value="simulate">
              <n-space vertical>
                <n-checkbox
                  v-for="option in benchmarkOptions"
                  :key="option.value"
                  :value="option.value"
                  :label="option.label"
                />
              </n-space>
            </n-checkbox-group>
          </n-form-item>
          <n-form-item label="Data inicial">
            <n-date-picker
              v-model:formatted-value="startDate"
              value-format="yyyy-MM-dd"
              type="date"
              style="width: 100%"
              @update:formatted-value="simulate"
            />
          </n-form-item>
          <n-form-item label="Data final (opcional)">
            <n-date-picker
              v-model:formatted-value="endDate"
              value-format="yyyy-MM-dd"
              type="date"
              clearable
              style="width: 100%"
              @update:formatted-value="simulate"
            />
          </n-form-item>
        </n-form>
      </n-card>
    </n-grid-item>

    <n-grid-item span="1 m:2">
      <n-card title="Rentabilidade acumulada" bordered content-style="padding: 24px" class="glass-card">
        <ComparisonChart :series="simulationStore.comparisonResult?.series ?? []" />
      </n-card>
    </n-grid-item>
  </n-grid>
</template>
