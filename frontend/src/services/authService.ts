import { api } from '@/services/api'
import type { AccessTokenResponse, User } from '@/types/user'

export const authService = {
  register(payload: { email: string; password: string; full_name: string }) {
    return api.post<AccessTokenResponse>('/auth/register', payload).then((r) => r.data)
  },
  login(payload: { email: string; password: string }) {
    return api.post<AccessTokenResponse>('/auth/login', payload).then((r) => r.data)
  },
  refresh() {
    return api.post<AccessTokenResponse>('/auth/refresh').then((r) => r.data)
  },
  logout() {
    return api.post('/auth/logout')
  },
  me() {
    return api.get<User>('/users/me').then((r) => r.data)
  },
  forgotPassword(email: string) {
    return api.post('/auth/forgot-password', { email })
  },
  resetPassword(payload: { token: string; new_password: string }) {
    return api.post('/auth/reset-password', payload)
  },
  googleLoginUrl() {
    return `${api.defaults.baseURL}/auth/google/login`
  },
}
