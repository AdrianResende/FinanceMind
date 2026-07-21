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
  <v-container>
    <div class="d-flex align-center justify-space-between mb-4 flex-wrap ga-2">
      <h1 class="text-h5 font-weight-bold">Olá, {{ auth.user?.full_name }}</h1>
      <v-btn-toggle v-model="periodModel" color="primary" density="comfortable" mandatory>
        <v-btn v-for="option in periodOptions" :key="option.value" :value="option.value">
          {{ option.label }}
        </v-btn>
      </v-btn-toggle>
    </div>

    <v-alert v-if="dashboardStore.error" type="error" density="compact" class="mb-4">
      {{ dashboardStore.error }}
    </v-alert>

    <v-row class="mb-2">
      <v-col cols="12" sm="4">
        <PatrimonioCard :total="dashboardStore.totalCurrent" :performance="dashboardStore.performance" />
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="7">
        <RentabilidadeChart :series="dashboardStore.benchmarks" />
      </v-col>
      <v-col cols="12" md="5">
        <AlocacaoChart :items="dashboardStore.allocation" />
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="7">
        <EvolucaoPatrimonialChart :points="dashboardStore.performance" />
      </v-col>
      <v-col cols="12" md="5">
        <TopMoversTable :data="dashboardStore.topMovers" />
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <DividendosChart :dividends="dashboardStore.dividends" />
      </v-col>
    </v-row>
  </v-container>
</template>
