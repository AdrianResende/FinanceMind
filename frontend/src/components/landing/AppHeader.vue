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
  <v-app-bar flat color="surface" border>
    <v-container class="d-flex align-center">
      <span class="text-h6 font-weight-bold">FinanceMind</span>
      <v-spacer />
      <v-btn
        v-for="link in links"
        :key="link.target"
        variant="text"
        class="d-none d-md-inline-flex"
        :href="link.target"
      >
        {{ link.label }}
      </v-btn>
      <v-btn variant="text" @click="router.push({ name: 'login' })">Entrar</v-btn>
      <v-btn color="primary" @click="router.push({ name: 'register' })">Criar conta</v-btn>
    </v-container>
  </v-app-bar>
</template>
