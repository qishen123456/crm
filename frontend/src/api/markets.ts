import { apiClient } from './client'

export interface Market {
  code: string
  name: string
  flag: string
}

export async function listMarkets(): Promise<Market[]> {
  const { data } = await apiClient.get('/markets')
  return data as Market[]
}
