type AuthContext = {
  userId: string
  tenantId: string
}

type RequestBody = {
  tenant_id: string
}

export async function getTenantData(
  auth: AuthContext,
  body: RequestBody
) {
  void auth
  return loadTenantData(body.tenant_id)
}

declare function loadTenantData(tenantId: string): Promise<unknown>
