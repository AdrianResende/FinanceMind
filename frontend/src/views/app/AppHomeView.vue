<script setup lang="ts">
import { computed, onMounted } from 'vue'

import AlocacaoChart from '@/components/dashboard/AlocacaoChart.vue'
import DividendosChart from '@/components/dashboard/DividendosChart.vue'
import EvolucaoPatrimonialChart from '@/components/dashboard/EvolucaoPatrimonialChart.vue'
import PatrimonioCard from '@/components/dashboard/PatrimonioCard.vue'
import RentabilidadeChart from '@/components/dashboard/RentabilidadeChart.vue'
import TopMoversTable from '@/components/dashboard/TopMoversTable.vue'
import { useAuthStore } from '@/stores/auth'
import { useDashboardStore, type DashboardPeriod } from '@/stores/dashboard'

const auth = useAuthStore()
const dashboardStore = useDashboardStore()

const periodOptions: { label: string; value: DashboardPeriod }[] = [
  { label: '1M', value: '1m' },
  { label: '3M', value: '3m' },
  { label: '6M', value: '6m' },
  { label: '1A', value: '1a' },
]

const periodModel = computed({
  get: () => dashboardStore.period,
  set: (value: DashboardPeriod) => dashboardStore.setPeriod(value),
})

onMounted(() => {
  dashboardStore.loadDashboard()
})
</script>

<template>
  <div>
    <div class="dashboard-header mb-6">
      <h1 class="text-section-title">Olá, {{ auth.user?.full_name }}</h1>
      <n-radio-group v-model:value="periodModel" name="period">
        <n-radio-button v-for="option in periodOptions" :key="option.value" :value="option.value">
          {{ option.label }}
        </n-radio-button>
      </n-radio-group>
    </div>

    <n-alert v-if="dashboardStore.error" type="error" class="mb-4">
      {{ dashboardStore.error }}
    </n-alert>

    <n-grid :x-gap="24" :y-gap="24" cols="1 m:3" responsive="screen" class="mb-6">
      <n-grid-item>
        <PatrimonioCard :total="dashboardStore.totalCurrent" :performance="dashboardStore.performance" />
      </n-grid-item>
    </n-grid>

    <n-grid :x-gap="24" :y-gap="24" cols="1 m:12" responsive="screen" class="mb-6">
      <n-grid-item span="1 m:7">
        <RentabilidadeChart :series="dashboardStore.benchmarks" />
      </n-grid-item>
      <n-grid-item span="1 m:5">
        <AlocacaoChart :items="dashboardStore.allocation" />
      </n-grid-item>
    </n-grid>

    <n-grid :x-gap="24" :y-gap="24" cols="1 m:12" responsive="screen" class="mb-6">
      <n-grid-item span="1 m:7">
        <EvolucaoPatrimonialChart :points="dashboardStore.performance" />
      </n-grid-item>
      <n-grid-item span="1 m:5">
        <TopMoversTable :data="dashboardStore.topMovers" />
      </n-grid-item>
    </n-grid>

    <n-grid :x-gap="24" :y-gap="24" cols="1">
      <n-grid-item>
        <DividendosChart :dividends="dashboardStore.dividends" />
      </n-grid-item>
    </n-grid>
  </div>
</template>

<style scoped>
.dashboard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: var(--space-3);
}
</style>
