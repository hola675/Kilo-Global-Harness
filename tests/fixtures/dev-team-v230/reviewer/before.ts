type AuthContext = {
  userId: string
  tenantId: string
}

export async function getTenantData(auth: AuthContext) {
  return loadTenantData(auth.tenantId)
}

declare function loadTenantData(tenantId: string): Promise<unknown>
