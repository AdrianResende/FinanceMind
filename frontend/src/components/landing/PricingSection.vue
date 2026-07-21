<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const plans = [
  {
    name: 'Free',
    price: 'R$ 0',
    period: '/sempre',
    highlight: false,
    features: [
      'Até 10 posições na carteira',
      'Lançamentos ilimitados',
      'Dashboard e benchmarks completos',
      'Glossário e simuladores completos',
      '15 mensagens de IA por mês',
    ],
  },
  {
    name: 'Premium',
    price: 'em breve',
    period: '',
    highlight: true,
    features: [
      'Posições ilimitadas na carteira',
      'Dashboard e benchmarks completos',
      'Glossário e simuladores completos',
      'Chat de IA ilimitado (fair-use)',
      'Suporte prioritário',
    ],
  },
]
</script>

<template>
  <section id="planos" class="page-shell section-py">
    <h2 class="text-section-title text-center mb-8">Planos</h2>

    <n-grid :x-gap="24" :y-gap="24" cols="1 m:2" responsive="screen" class="pricing-grid">
      <n-grid-item v-for="plan in plans" :key="plan.name">
        <div class="pricing-card-wrap">
          <n-tag v-if="plan.highlight" type="success" round :bordered="false" class="pricing-badge">
            Mais popular
          </n-tag>
          <n-card
            bordered
            hoverable
            content-style="padding: 24px"
            class="glass-card h-100"
            :class="{ 'glass-card--tint': plan.highlight }"
          >
            <h3 class="text-title mb-1">{{ plan.name }}</h3>
            <p class="pricing-price mb-4">
              {{ plan.price }}<span class="text-body pricing-period">{{ plan.period }}</span>
            </p>

            <ul class="pricing-features mb-6">
              <li v-for="feature in plan.features" :key="feature">
                <MdiIcon name="check" :size="18" :color="plan.highlight ? '#7fe0c8' : undefined" />
                <span>{{ feature }}</span>
              </li>
            </ul>

            <n-button
              block
              round
              size="large"
              :type="plan.highlight ? undefined : 'primary'"
              :color="plan.highlight ? '#ffffff' : undefined"
              :text-color="plan.highlight ? 'var(--brand-primary)' : undefined"
              @click="router.push({ name: 'register' })"
            >
              Começar agora
            </n-button>
          </n-card>
        </div>
      </n-grid-item>
    </n-grid>
  </section>
</template>

<style scoped>
.pricing-grid {
  max-width: 760px;
  margin-inline: auto;
}

.pricing-card-wrap {
  position: relative;
  height: 100%;
}

.pricing-badge {
  position: absolute;
  top: -14px;
  right: 24px;
  z-index: 1;
  font-weight: 600;
}

.pricing-price {
  font-size: 2.25rem;
  font-weight: 700;
  color: var(--ink-1);
}

.glass-card--tint .pricing-price {
  color: #fff;
}

.pricing-period {
  font-size: 0.9rem;
  margin-inline-start: var(--space-1);
}

.pricing-features {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.pricing-features li {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  font-size: 0.9375rem;
}
</style>
