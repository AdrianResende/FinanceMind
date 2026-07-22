export interface User {
  id: string
  email: string
  full_name: string
  plan: 'free' | 'premium'
  email_verified: boolean
  auth_provider: 'local' | 'google'
  created_at: string
}

export interface AccessTokenResponse {
  access_token: string
  token_type: string
  user: User
}
