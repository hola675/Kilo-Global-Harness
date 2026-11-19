export async function loadTenantData(tenantId: string) {
  return { tenantId, records: [] as unknown[] }
}
