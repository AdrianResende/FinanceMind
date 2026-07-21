import axios from 'axios'

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api/v1',
  withCredentials: true,
})

let accessTokenGetter: () => string | null = () => null
let onUnauthorized: () => void = () => {}

export function configureApiAuth(getter: () => string | null, unauthorizedHandler: () => void) {
  accessTokenGetter = getter
  onUnauthorized = unauthorizedHandler
}

api.interceptors.request.use((config) => {
  const token = accessTokenGetter()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      onUnauthorized()
    }
    return Promise.reject(error)
  },
)
