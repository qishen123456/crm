import { apiClient } from './client'

export interface OrderItem {
  id: string
  sku: string
  name: string
  qty: number
  unitPrice: number
}

export interface Order {
  id: string
  orderNumber: string
  piNumber: string
  accountId: string
  requestedById?: string
  subtotalUsd: number
  status: string
  orderType?: string
  orderKind?: string
  poStatus?: string
  createdAt?: string
  shippedAt?: string
  items: OrderItem[]
}

function fromApiItem(data: Record<string, unknown>): OrderItem {
  return {
    id: data.id as string,
    sku: data.sku as string,
    name: data.name as string,
    qty: data.qty as number,
    unitPrice: Number(data.unit_price_usd ?? 0),
  }
}

function fromApi(data: Record<string, unknown>): Order {
  return {
    id: data.id as string,
    orderNumber: data.order_number as string,
    piNumber: (data.pi_number as string) || '',
    accountId: data.account_id as string,
    requestedById: (data.requested_by_id as string) || undefined,
    subtotalUsd: Number(data.subtotal_usd ?? 0),
    status: data.status as string,
    orderType: (data.order_type as string) || undefined,
    orderKind: (data.order_kind as string) || undefined,
    poStatus: (data.po_status as string) || undefined,
    createdAt: (data.created_at as string) || undefined,
    shippedAt: (data.shipped_at as string) || undefined,
    items: ((data.items as Record<string, unknown>[]) || []).map(fromApiItem),
  }
}

export async function listOrders(): Promise<Order[]> {
  const { data } = await apiClient.get('/orders')
  return (data as Record<string, unknown>[]).map(fromApi)
}

export async function getOrder(id: string): Promise<Order> {
  const { data } = await apiClient.get(`/orders/${id}`)
  return fromApi(data as Record<string, unknown>)
}
