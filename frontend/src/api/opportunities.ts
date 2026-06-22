import { apiClient } from './client'

export type OpportunityStage = 'prospect' | 'qualify' | 'proposal' | 'negotiate' | 'closedWon'

export interface Opportunity {
  id: string
  accountId: string
  companyName: string
  regionCode: string
  tags: string
  amount: string
  ownerName: string
  stage: OpportunityStage
  isNoFollowUp: boolean
  winType?: 'first' | 'reorder' | null
  createdAt?: string
  updatedAt?: string
}

export interface OpportunityCreatePayload {
  accountId: string
  companyName: string
  regionCode: string
  tags: string
  amount: string
  ownerName: string
  stage: OpportunityStage
  isNoFollowUp?: boolean
  winType?: 'first' | 'reorder' | null
}

export interface OpportunityUpdatePayload {
  accountId?: string
  companyName?: string
  regionCode?: string
  tags?: string
  amount?: string
  ownerName?: string
  stage?: OpportunityStage
  isNoFollowUp?: boolean
  winType?: 'first' | 'reorder' | null
}

function fromApi(data: Record<string, unknown>): Opportunity {
  return {
    id: data.id as string,
    accountId: data.account_id as string,
    companyName: data.company_name as string,
    regionCode: data.region_code as string,
    tags: data.tags as string,
    amount: data.amount as string,
    ownerName: data.owner_name as string,
    stage: data.stage as OpportunityStage,
    isNoFollowUp: Boolean(data.is_no_follow_up),
    winType: (data.win_type as Opportunity['winType']) || null,
    createdAt: data.created_at as string | undefined,
    updatedAt: data.updated_at as string | undefined,
  }
}

function toApi(payload: OpportunityCreatePayload | OpportunityUpdatePayload): Record<string, unknown> {
  return {
    account_id: payload.accountId,
    company_name: payload.companyName,
    region_code: payload.regionCode,
    tags: payload.tags,
    amount: payload.amount,
    owner_name: payload.ownerName,
    stage: payload.stage,
    is_no_follow_up: payload.isNoFollowUp,
    win_type: payload.winType,
  }
}

export async function listOpportunities(): Promise<Opportunity[]> {
  const { data } = await apiClient.get('/opportunities')
  return (data as Record<string, unknown>[]).map(fromApi)
}

export async function getOpportunity(id: string): Promise<Opportunity> {
  const { data } = await apiClient.get(`/opportunities/${id}`)
  return fromApi(data as Record<string, unknown>)
}

export async function createOpportunity(payload: OpportunityCreatePayload): Promise<Opportunity> {
  const { data } = await apiClient.post('/opportunities', toApi(payload))
  return fromApi(data as Record<string, unknown>)
}

export async function updateOpportunity(id: string, payload: OpportunityUpdatePayload): Promise<Opportunity> {
  const { data } = await apiClient.patch(`/opportunities/${id}`, toApi(payload))
  return fromApi(data as Record<string, unknown>)
}

export async function deleteOpportunity(id: string): Promise<void> {
  await apiClient.delete(`/opportunities/${id}`)
}
