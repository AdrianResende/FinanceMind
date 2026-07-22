import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

import { configureApiAuth } from '@/services/api'
import { authService } from '@/services/authService'
import type { User } from '@/types/user'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref<string | null>(null)
  const user = ref<User | null>(null)
  const isDemoMode = ref(false)
  const isAuthenticated = computed(() => accessToken.value !== null && user.value !== null)

  function applySession(token: string, sessionUser: User) {
    accessToken.value = token
    user.value = sessionUser
  }

  function clear() {
    accessToken.value = null
    user.value = null
    isDemoMode.value = false
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
    if (isDemoMode.value) {
      clear()
      return
    }
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

  function enterDemoMode() {
    isDemoMode.value = true
    applySession('demo-token', {
      id: 'demo-user',
      email: 'demo@financemind.app',
      full_name: 'Usuário Demonstração',
      plan: 'premium',
      email_verified: true,
      auth_provider: 'local',
      created_at: new Date().toISOString(),
    })
  }

  async function loadCurrentUser() {
    user.value = await authService.me()
  }

  async function updateProfile(fullName: string) {
    if (isDemoMode.value) {
      throw new Error('Ação indisponível em modo demonstração.')
    }
    user.value = await authService.updateProfile({ full_name: fullName })
  }

  async function changePassword(currentPassword: string, newPassword: string) {
    if (isDemoMode.value) {
      throw new Error('Ação indisponível em modo demonstração.')
    }
    await authService.changePassword({ current_password: currentPassword, new_password: newPassword })
  }

  async function deleteAccount() {
    if (isDemoMode.value) {
      throw new Error('Ação indisponível em modo demonstração.')
    }
    await authService.deleteAccount()
    clear()
  }

  configureApiAuth(
    () => accessToken.value,
    () => clear(),
  )

  return {
    accessToken,
    user,
    isDemoMode,
    isAuthenticated,
    login,
    register,
    logout,
    tryRestoreSession,
    setAccessTokenFromOAuth,
    loadCurrentUser,
    enterDemoMode,
    updateProfile,
    changePassword,
    deleteAccount,
  }
})
