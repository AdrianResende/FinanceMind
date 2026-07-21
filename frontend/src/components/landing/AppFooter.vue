<template>
  <footer class="app-footer">
    <div class="page-shell app-footer__inner">
      <span class="text-title" style="font-size: 1rem">FinanceMind</span>
      <span class="text-muted">Conteúdo educativo, não constitui recomendação de investimento.</span>
      <span class="text-muted">© {{ new Date().getFullYear() }} FinanceMind. Todos os direitos reservados.</span>
    </div>
  </footer>
</template>

<style scoped>
.app-footer {
  border-top: 1px solid rgba(15, 76, 100, 0.1);
  background: rgba(255, 255, 255, 0.5);
}

.app-footer__inner {
  padding-block: var(--space-8);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-1);
  text-align: center;
}
</style>
