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
  <v-container id="planos" class="py-12">
    <h2 class="text-h4 font-weight-bold text-center mb-10">Planos</h2>
    <v-row justify="center">
      <v-col v-for="plan in plans" :key="plan.name" cols="12" sm="8" md="4">
        <v-card
          class="pa-6 h-100"
          :variant="plan.highlight ? 'elevated' : 'outlined'"
          :color="plan.highlight ? 'primary' : undefined"
        >
          <h3 class="text-h5 font-weight-bold mb-1">{{ plan.name }}</h3>
          <p class="text-h4 font-weight-bold mb-1">
            {{ plan.price }}<span class="text-body-2">{{ plan.period }}</span>
          </p>
          <v-list :class="plan.highlight ? 'bg-transparent' : ''" density="compact">
            <v-list-item v-for="feature in plan.features" :key="feature" :title="feature">
              <template #prepend>
                <v-icon icon="mdi-check" size="18" />
              </template>
            </v-list-item>
          </v-list>
          <v-btn
            block
            class="mt-4"
            :color="plan.highlight ? 'white' : 'primary'"
            :variant="plan.highlight ? 'flat' : 'elevated'"
            @click="router.push({ name: 'register' })"
          >
            Começar agora
          </v-btn>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
