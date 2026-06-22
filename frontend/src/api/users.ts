import { apiClient } from './client'

export interface User {
  id: string
  name: string
  email: string
  role: string
  department: string
  marketCode?: string
  avatar: string
  status: string
}

function fromApi(data: Record<string, unknown>): User {
  return {
    id: data.id as string,
    name: data.name as string,
    email: data.email as string,
    role: data.role as string,
    department: data.department as string,
    marketCode: (data.market_code as string) || undefined,
    avatar: (data.avatar as string) || '',
    status: data.status as string,
  }
}

export async function listUsers(): Promise<User[]> {
  const { data } = await apiClient.get('/users')
  return (data as Record<string, unknown>[]).map(fromApi)
}
