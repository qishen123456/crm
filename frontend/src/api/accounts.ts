import { apiClient } from './client'

export interface Account {
  id: string
  code: string
  name: string
  market: string
  ownerId: string
  annualTargetUsd: number
  yearToDateUsd: number
  contractStatus: string
  contractExpiresAt?: string
  businessType?: string
  opportunityNotes?: string
  customerResources?: string
  nextDigDirections?: string
}

function fromApi(data: Record<string, unknown>): Account {
  return {
    id: data.id as string,
    code: data.code as string,
    name: data.name as string,
    market: data.market_code as string,
    ownerId: (data.owner_id as string) || '',
    annualTargetUsd: Number(data.annual_target_usd ?? 0),
    yearToDateUsd: Number(data.year_to_date_usd ?? 0),
    contractStatus: (data.contract_status as string) || 'active',
    contractExpiresAt: (data.contract_expires_at as string) || undefined,
    businessType: (data.business_type as string) || undefined,
    opportunityNotes: (data.opportunity_notes as string) || undefined,
    customerResources: (data.customer_resources as string) || undefined,
    nextDigDirections: (data.next_dig_directions as string) || undefined,
  }
}

export async function listAccounts(): Promise<Account[]> {
  const { data } = await apiClient.get('/accounts')
  return (data as Record<string, unknown>[]).map(fromApi)
}

export async function getAccount(id: string): Promise<Account> {
  const { data } = await apiClient.get(`/accounts/${id}`)
  return fromApi(data as Record<string, unknown>)
}
