<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const links = [
  { label: 'Sobre', target: '#sobre' },
  { label: 'Benefícios', target: '#beneficios' },
  { label: 'Recursos', target: '#recursos' },
  { label: 'Planos', target: '#planos' },
  { label: 'FAQ', target: '#faq' },
  { label: 'Contato', target: '#contato' },
]
</script>

<template>
  <header class="app-header">
    <div class="page-shell app-header__inner">
      <span class="text-title app-header__brand">FinanceMind</span>

      <nav class="app-header__nav">
        <a v-for="link in links" :key="link.target" :href="link.target" class="app-header__link">
          {{ link.label }}
        </a>
      </nav>

      <div class="app-header__actions">
        <n-button quaternary @click="router.push({ name: 'login' })">Entrar</n-button>
        <n-button type="primary" round @click="router.push({ name: 'register' })">Criar conta</n-button>
      </div>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  position: sticky;
  top: 0;
  z-index: 20;
  background: rgba(255, 255, 255, 0.65);
  backdrop-filter: blur(16px) saturate(160%);
  -webkit-backdrop-filter: blur(16px) saturate(160%);
  border-bottom: 1px solid rgba(255, 255, 255, 0.6);
}

.app-header__inner {
  height: 72px;
  display: flex;
  align-items: center;
  gap: var(--space-6);
}

.app-header__brand {
  color: var(--brand-primary);
}

.app-header__nav {
  display: none;
  align-items: center;
  gap: var(--space-6);
  margin-inline-start: var(--space-8);
  flex: 1;
}

.app-header__link {
  color: var(--ink-2);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  transition: color 0.15s ease;
}

.app-header__link:hover {
  color: var(--brand-primary);
}

.app-header__actions {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-inline-start: auto;
}

@media (min-width: 960px) {
  .app-header__nav {
    display: flex;
  }
}
</style>
