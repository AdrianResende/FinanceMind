<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()
const drawer = ref(true)

const menuItems = [
  { title: 'Home', icon: 'mdi-view-dashboard-outline', to: { name: 'app-home' } },
  { title: 'Carteira', icon: 'mdi-briefcase-outline', to: { name: 'portfolio-home' } },
  { title: 'Mercado', icon: 'mdi-chart-areaspline', to: null },
  { title: 'Aprendizado', icon: 'mdi-book-education-outline', to: null },
  { title: 'Simulações', icon: 'mdi-calculator-variant-outline', to: null },
  { title: 'IA', icon: 'mdi-robot-outline', to: null },
  { title: 'Perfil', icon: 'mdi-account-outline', to: null },
  { title: 'Configurações', icon: 'mdi-cog-outline', to: null },
]

async function onLogout() {
  await auth.logout()
  router.push({ name: 'landing' })
}
</script>

<template>
  <v-navigation-drawer v-model="drawer">
    <v-list-item title="FinanceMind" class="font-weight-bold py-4" />
    <v-divider />
    <v-list nav>
      <v-list-item
        v-for="item in menuItems"
        :key="item.title"
        :prepend-icon="item.icon"
        :title="item.title"
        :to="item.to ?? undefined"
        :disabled="!item.to"
      />
    </v-list>
  </v-navigation-drawer>

  <v-app-bar flat border>
    <v-app-bar-nav-icon @click="drawer = !drawer" />
    <v-chip v-if="auth.isDemoMode" color="warning" variant="tonal" prepend-icon="mdi-flask-outline" class="ml-2">
      Modo demonstração
    </v-chip>
    <v-spacer />
    <span class="text-body-2 mr-4">{{ auth.user?.full_name }} · plano {{ auth.user?.plan }}</span>
    <v-btn variant="text" prepend-icon="mdi-logout" @click="onLogout">Sair</v-btn>
  </v-app-bar>

  <v-main>
    <RouterView />
  </v-main>
</template>
