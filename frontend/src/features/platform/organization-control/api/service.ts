import { apiClient } from "@/core/api";

import type {
  OrganizationControlFeature,
  OrganizationControlModule,
  OrganizationControlPlaneSnapshot,
} from "../domain";

import { organizationControlEndpoints } from "./endpoints";

export async function fetchOrganizationControlPlane(): Promise<OrganizationControlPlaneSnapshot> {
  const response = await apiClient.get<OrganizationControlPlaneSnapshot>(
    organizationControlEndpoints.snapshot,
  );

  return response.data;
}

export async function toggleOrganizationModule(input: {
  id: string;
  enabled: boolean;
}): Promise<OrganizationControlModule> {
  const response = await apiClient.patch<OrganizationControlModule>(
    organizationControlEndpoints.moduleToggle(input.id),
    { enabled: input.enabled },
  );

  return response.data;
}

export async function toggleOrganizationFeature(input: {
  id: string;
  enabled: boolean;
}): Promise<OrganizationControlFeature> {
  const response = await apiClient.patch<OrganizationControlFeature>(
    organizationControlEndpoints.featureToggle(input.id),
    { enabled: input.enabled },
  );

  return response.data;
}
