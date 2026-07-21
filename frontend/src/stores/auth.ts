import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref<string | null>(null)
  const isAuthenticated = ref(false)

  function setAccessToken(token: string) {
    accessToken.value = token
    isAuthenticated.value = true
  }

  function clear() {
    accessToken.value = null
    isAuthenticated.value = false
  }

  return { accessToken, isAuthenticated, setAccessToken, clear }
})
