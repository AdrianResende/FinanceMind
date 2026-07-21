<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<template>
  <div class="hero-bg">
    <div class="page-shell hero-inner">
      <n-tag type="success" round :bordered="false" size="medium" class="hero-tag">
        Beta gratuito
      </n-tag>
      <h1 class="text-display hero-title">
        Entenda seus investimentos. Acompanhe sua carteira. Cresça com confiança.
      </h1>
      <p class="text-lead hero-subtitle">
        FinanceMind ensina como funcionam Ações, FIIs, ETFs, Tesouro Direto e outros investimentos,
        e ajuda você a acompanhar sua carteira com clareza — sem jargão, sem achismo.
      </p>
      <n-space justify="center" :size="16" class="hero-actions">
        <n-button type="primary" size="large" round @click="router.push({ name: 'register' })">
          Criar conta grátis
        </n-button>
        <n-button size="large" round tag="a" href="#recursos"> Ver recursos </n-button>
      </n-space>
      <p class="text-muted hero-disclaimer">
        Conteúdo educativo. Não é recomendação de investimento.
      </p>
    </div>
  </div>
</template>

<style scoped>
.hero-bg {
  padding-block: var(--space-24);
  background:
    radial-gradient(circle at 50% 0%, rgba(14, 156, 143, 0.16), transparent 55%),
    radial-gradient(circle at 85% 15%, rgba(15, 76, 100, 0.1), transparent 50%);
}

.hero-inner {
  max-width: 760px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.hero-tag {
  margin-bottom: var(--space-4);
}

.hero-title {
  margin-bottom: var(--space-4);
}

.hero-subtitle {
  margin-bottom: var(--space-8);
}

.hero-actions {
  margin-bottom: var(--space-4);
}

@media (max-width: 960px) {
  .hero-bg {
    padding-block: var(--space-16);
  }
}
</style>
