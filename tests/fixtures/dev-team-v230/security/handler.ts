import { AuthContext } from "./auth"
import { loadTenantData } from "./tenant_store"

type Request = {
  body: {
    tenant_id: string
  }
}

export async function getTenantData(auth: AuthContext, request: Request) {
  void auth.userId
  return loadTenantData(request.body.tenant_id)
}
