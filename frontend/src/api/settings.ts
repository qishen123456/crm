import { apiClient } from './client'

export interface RolePermission {
  permission_code: string
  granted: boolean
}

export interface Role {
  code: string
  name_en: string
  name_zh: string
  record_access_scope: string
  is_system: boolean
  sort_order: number
  is_active: boolean
  permissions: RolePermission[]
}

export async function listRoles(): Promise<Role[]> {
  const { data } = await apiClient.get('/settings/roles')
  return data as Role[]
}

export async function updateRole(
  code: string,
  payload: { record_access_scope?: string; permissions?: Record<string, boolean> }
): Promise<Role> {
  const { data } = await apiClient.patch(`/settings/roles/${code}`, payload)
  return data as Role
}
