import { API_BASE_URL } from "@/core/api/config";
import { ENDPOINTS } from "./endpoints";
import { apiGet, apiPatch } from "./http";

export type PlatformBootstrap = {
  user: {
    id: string;
    email: string;
    first_name?: string;
    last_name?: string;
    name?: string;
  };

  tenant: {
    id: string;
    name: string;
    tenant_type: string;
    status: string;
  } | null;

  organization: {
    id: string;
    name: string;
    category?: string;
    type?: string;
    size?: string;
  } | null;

  employee: {
    id: string;
    employee_code: string;
  } | null;

  platform_roles: string[];
  organization_roles: string[];
  permissions: string[];

  modules: Array<{
    identifier: string;
    name: string;
    display_name: string;
    description: string;
    version: string;
    category: string;
    route: string;
    api_prefix: string;
    icon: string;
    permissions: string[];
    enabled: boolean;
    system: boolean;
    tenant_scoped: boolean;
    order: number;
    tags: string[];
    feature_flags: string[];
  }>;

  navigation: Array<{
    title: string;
    route: string;
    icon: string;
    category: string;
    permissions: string[];
    order: number;
  }>;

  dashboard: Array<{
    key: string;
    title: string;
    description: string;
    icon: string;
    route: string;
    category: string;
    order: number;
  }>;

  branding: Record<string, unknown>;
  feature_flags: Record<string, unknown>;

  subscription: {
    status: string;
    auto_renew: boolean;
    plan: {
      name: string;
      code: string;
      billing_cycle: string;
    };
  } | null;

  preferences: Record<string, unknown> | null;
};

export async function getPlatformBootstrap(): Promise<PlatformBootstrap> {
  const response =
    await apiGet<PlatformBootstrap>(
      ENDPOINTS.runtime.bootstrap,
    );

  return response.data;
}

export async function getOrganizationControlPlane(): Promise<unknown> {
  const token =
    typeof window !== "undefined"
      ? window.localStorage.getItem(
          "datavion_access_token",
        )
      : null;

  const response =
    await fetch(
      `${API_BASE_URL}${ENDPOINTS.controlPlane.snapshot}`,
      {
        method: "GET",
        headers: {
          Accept:
            "application/json",
          ...(token
            ? {
                Authorization:
                  `Bearer ${token}`,
              }
            : {}),
        },
        credentials: "include",
        cache: "no-store",
      },
    );

  const body =
    await response.json();

  if (!response.ok) {
    throw new Error(
      typeof body?.detail ===
        "string"
        ? body.detail
        : `Organization control-plane request failed (${response.status})`,
    );
  }

  return body;
}

export async function toggleOrganizationModule(
  moduleId: string,
  enabled: boolean,
): Promise<unknown> {
  return apiPatch<unknown>(
    ENDPOINTS.controlPlane.toggleModule(
      moduleId,
    ),
    {
      enabled,
    },
  );
}

export async function toggleOrganizationFeature(
  featureId: string,
  enabled: boolean,
): Promise<unknown> {
  return apiPatch<unknown>(
    ENDPOINTS.controlPlane.toggleFeature(
      featureId,
    ),
    {
      enabled,
    },
  );
}
