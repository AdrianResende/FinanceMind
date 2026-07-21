<script setup lang="ts">
import { h, ref } from 'vue'
import { RouterLink, RouterView, useRouter } from 'vue-router'
import type { MenuOption } from 'naive-ui'

import MdiIcon from '@/components/common/MdiIcon.vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()
const collapsed = ref(false)

const rawMenuItems = [
  { title: 'Home', icon: 'view-dashboard-outline', to: { name: 'app-home' } },
  { title: 'Carteira', icon: 'briefcase-outline', to: { name: 'portfolio-home' } },
  { title: 'Mercado', icon: 'chart-areaspline', to: null },
  { title: 'Aprendizado', icon: 'book-education-outline', to: null },
  { title: 'Simulações', icon: 'calculator-variant-outline', to: null },
  { title: 'IA', icon: 'robot-outline', to: null },
  { title: 'Perfil', icon: 'account-outline', to: null },
  { title: 'Configurações', icon: 'cog-outline', to: null },
] as const

function renderIcon(icon: string) {
  return () => h(MdiIcon, { name: icon, size: 18 })
}

const menuOptions: MenuOption[] = rawMenuItems.map((item) => ({
  key: item.title,
  icon: renderIcon(item.icon),
  disabled: !item.to,
  label: item.to
    ? () => h(RouterLink, { to: item.to! }, { default: () => item.title })
    : item.title,
}))

async function onLogout() {
  await auth.logout()
  router.push({ name: 'landing' })
}
</script>

<template>
  <n-layout has-sider style="min-height: 100vh; background: transparent">
    <n-layout-sider
      bordered
      collapse-mode="width"
      :collapsed-width="64"
      :width="232"
      :collapsed="collapsed"
      show-trigger
      class="app-sider"
      @collapse="collapsed = true"
      @expand="collapsed = false"
    >
      <div class="app-sider__brand">
        <span v-if="!collapsed" class="text-title">FinanceMind</span>
        <span v-else class="text-title">FM</span>
      </div>
      <n-menu :options="menuOptions" :collapsed="collapsed" :collapsed-width="64" />
    </n-layout-sider>

    <n-layout>
      <n-layout-header bordered class="app-topbar">
        <n-tag v-if="auth.isDemoMode" type="warning" round :bordered="false">
          <template #icon><MdiIcon name="flask-outline" :size="14" /></template>
          Modo demonstração
        </n-tag>
        <div class="app-topbar__spacer" />
        <span class="text-body app-topbar__user">
          {{ auth.user?.full_name }} · plano {{ auth.user?.plan }}
        </span>
        <n-button quaternary @click="onLogout">
          <template #icon><MdiIcon name="logout" :size="16" /></template>
          Sair
        </n-button>
      </n-layout-header>

      <n-layout-content class="app-content">
        <RouterView />
      </n-layout-content>
    </n-layout>
  </n-layout>
</template>

<style scoped>
.app-sider {
  background: rgba(255, 255, 255, 0.7) !important;
  backdrop-filter: blur(16px) saturate(160%);
}

.app-sider__brand {
  height: 64px;
  display: flex;
  align-items: center;
  padding-inline: var(--space-6);
  color: var(--brand-primary);
}

.app-topbar {
  height: 64px;
  display: flex;
  align-items: center;
  padding-inline: var(--space-6);
  background: rgba(255, 255, 255, 0.7) !important;
  backdrop-filter: blur(16px) saturate(160%);
}

.app-topbar__spacer {
  flex: 1;
}

.app-topbar__user {
  margin-inline-end: var(--space-4);
}

.app-content {
  padding: var(--space-6);
  min-height: calc(100vh - 64px);
}
</style>
