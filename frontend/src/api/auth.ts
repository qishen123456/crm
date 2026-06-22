import { apiClient } from './client'

export interface AuthUser {
  id: string
  name: string
  email: string
  role_code: string
  role_name?: string
  department: string
  market_code?: string
  avatar: string
  status: string
  permissions: string[]
  record_access_scope?: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: AuthUser
}

export async function login(email: string, password: string): Promise<LoginResponse> {
  const { data } = await apiClient.post('/auth/login', { email, password })
  return data as LoginResponse
}

export async function me(): Promise<AuthUser> {
  const { data } = await apiClient.get('/auth/me')
  return data as AuthUser
}

export async function switchRole(roleCode: string): Promise<LoginResponse> {
  const { data } = await apiClient.post('/auth/switch-role', { role_code: roleCode })
  return data as LoginResponse
}
