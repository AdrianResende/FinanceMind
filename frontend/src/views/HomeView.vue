<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<template>
  <v-container class="fill-height" fluid>
    <v-responsive class="d-flex align-center justify-center text-center">
      <h1 class="text-h3 font-weight-bold">{{ t('app.name') }}</h1>
      <p class="text-body-1 mt-2">Educação e acompanhamento de investimentos.</p>
    </v-responsive>
  </v-container>
</template>
