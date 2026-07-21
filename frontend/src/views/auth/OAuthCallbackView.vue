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
  <div class="oauth-loading">
    <n-spin size="large" />
  </div>
</template>

<style scoped>
.oauth-loading {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
