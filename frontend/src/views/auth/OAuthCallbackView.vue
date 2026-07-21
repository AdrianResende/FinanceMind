<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

onMounted(async () => {
  const token = route.query.access_token as string | undefined
  if (!token) {
    router.replace({ name: 'login' })
    return
  }

  auth.setAccessTokenFromOAuth(token)
  try {
    await auth.loadCurrentUser()
    router.replace({ name: 'app-home' })
  } catch {
    router.replace({ name: 'login' })
  }
})
</script>

<template>
  <v-container class="fill-height d-flex align-center justify-center">
    <v-progress-circular indeterminate color="primary" />
  </v-container>
</template>
