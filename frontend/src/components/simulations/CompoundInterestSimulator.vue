<script setup lang="ts">
import { onMounted, ref } from 'vue'

import CompoundInterestChart from '@/components/simulations/CompoundInterestChart.vue'
import { useSimulationStore } from '@/stores/simulation'

const simulationStore = useSimulationStore()

const initialAmount = ref(1000)
const monthlyAmount = ref(200)
const annualRatePct = ref(10)
const years = ref(10)

function formatCurrency(value: string) {
  return Number(value).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

async function simulate() {
  await simulationStore.runCompoundInterest({
    initial_amount: String(initialAmount.value ?? 0),
    monthly_amount: String(monthlyAmount.value ?? 0),
    annual_rate_pct: String(annualRatePct.value ?? 0),
    months: Math.round((years.value ?? 0) * 12),
  })
}

onMounted(simulate)
</script>

<template>
  <n-grid :x-gap="24" :y-gap="24" cols="1 m:3" responsive="screen">
    <n-grid-item>
      <n-card title="Parâmetros" bordered content-style="padding: 24px" class="glass-card">
        <n-form label-placement="top">
          <n-form-item label="Valor inicial">
            <n-input-number
              v-model:value="initialAmount"
              :min="0"
              :precision="2"
              style="width: 100%"
              @update:value="simulate"
            />
          </n-form-item>
          <n-form-item label="Aporte mensal">
            <n-input-number
              v-model:value="monthlyAmount"
              :min="0"
              :precision="2"
              style="width: 100%"
              @update:value="simulate"
            />
          </n-form-item>
          <n-form-item label="Taxa de juros (% a.a.)">
            <n-input-number
              v-model:value="annualRatePct"
              :min="0"
              :precision="2"
              style="width: 100%"
              @update:value="simulate"
            />
          </n-form-item>
          <n-form-item label="Prazo (anos)">
            <n-input-number
              v-model:value="years"
              :min="1"
              :max="50"
              style="width: 100%"
              @update:value="simulate"
            />
          </n-form-item>
        </n-form>
      </n-card>
    </n-grid-item>

    <n-grid-item span="1 m:2">
      <n-card title="Evolução do patrimônio" bordered content-style="padding: 24px" class="glass-card mb-6">
        <CompoundInterestChart :points="simulationStore.compoundInterestResult?.points ?? []" />
      </n-card>

      <n-grid v-if="simulationStore.compoundInterestResult" :x-gap="16" :y-gap="16" cols="1 s:3" responsive="screen">
        <n-grid-item>
          <n-card bordered content-style="padding: 20px" class="glass-card">
            <div class="text-muted" style="font-size: 0.8125rem">Total investido</div>
            <div class="text-title">
              {{ formatCurrency(simulationStore.compoundInterestResult.total_invested) }}
            </div>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card bordered content-style="padding: 20px" class="glass-card">
            <div class="text-muted" style="font-size: 0.8125rem">Juros acumulados</div>
            <div class="text-title" style="color: var(--brand-success)">
              {{ formatCurrency(simulationStore.compoundInterestResult.total_interest) }}
            </div>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card bordered content-style="padding: 20px" class="glass-card">
            <div class="text-muted" style="font-size: 0.8125rem">Total final</div>
            <div class="text-title">
              {{ formatCurrency(simulationStore.compoundInterestResult.final_amount) }}
            </div>
          </n-card>
        </n-grid-item>
      </n-grid>
    </n-grid-item>
  </n-grid>
</template>
