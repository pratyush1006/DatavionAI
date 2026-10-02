import { apiClient } from "@/core/api";
import { ENDPOINTS } from "@/lib/backend/endpoints";

export type TenantMembership = {
  id: string;
  name: string;
  tenant_type: string;
  status: string;
  role: "OWNER" | "MEMBER" | string;
  is_owner: boolean;
  joined_at: string;
};

export type TenantSelection = {
  tenant_id: string;
  name: string;
  tenant_type: string;
  role: "OWNER" | "MEMBER" | string;
};

export async function fetchMyTenants(): Promise<TenantMembership[]> {
  const response = await apiClient.get<TenantMembership[]>(
    ENDPOINTS.tenancy.myTenants,
  );
  return response.data;
}

export async function selectTenant(tenantId: string): Promise<TenantSelection> {
  const response = await apiClient.post<
    TenantSelection,
    { tenant_id: string }
  >(ENDPOINTS.tenancy.selectTenant, { tenant_id: tenantId });
  return response.data;
}
