import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

import { configureApiAuth } from '@/services/api'
import { authService } from '@/services/authService'
import type { User } from '@/types/user'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref<string | null>(null)
  const user = ref<User | null>(null)
  const isAuthenticated = computed(() => accessToken.value !== null && user.value !== null)

  function applySession(token: string, sessionUser: User) {
    accessToken.value = token
    user.value = sessionUser
  }

  function clear() {
    accessToken.value = null
    user.value = null
  }

  async function login(email: string, password: string) {
    const data = await authService.login({ email, password })
    applySession(data.access_token, data.user)
  }

  async function register(email: string, password: string, fullName: string) {
    const data = await authService.register({ email, password, full_name: fullName })
    applySession(data.access_token, data.user)
  }

  async function logout() {
    try {
      await authService.logout()
    } finally {
      clear()
    }
  }

  async function tryRestoreSession(): Promise<boolean> {
    try {
      const data = await authService.refresh()
      applySession(data.access_token, data.user)
      return true
    } catch {
      clear()
      return false
    }
  }

  function setAccessTokenFromOAuth(token: string) {
    accessToken.value = token
  }

  async function loadCurrentUser() {
    user.value = await authService.me()
  }

  configureApiAuth(
    () => accessToken.value,
    () => clear(),
  )

  return {
    accessToken,
    user,
    isAuthenticated,
    login,
    register,
    logout,
    tryRestoreSession,
    setAccessTokenFromOAuth,
    loadCurrentUser,
  }
})
