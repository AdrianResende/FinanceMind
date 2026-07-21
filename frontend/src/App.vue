<script setup lang="ts">
import { RouterView } from 'vue-router'
import { ptBR, datePtBR } from 'naive-ui'

import { themeOverrides } from '@/plugins/naive'
</script>

<template>
  <n-config-provider :theme-overrides="themeOverrides" :locale="ptBR" :date-locale="datePtBR">
    <n-loading-bar-provider>
      <n-dialog-provider>
        <n-message-provider>
          <RouterView />
        </n-message-provider>
      </n-dialog-provider>
    </n-loading-bar-provider>
  </n-config-provider>
</template>
