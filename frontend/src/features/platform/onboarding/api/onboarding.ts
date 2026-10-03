import { apiClient } from "@/core/api";

import type {
  OrganizationCatalog,
  OrganizationOnboardingResult,
  OrganizationOnboardingStatusItem,
  OrganizationRegistrationPayload,
  SaaSPlan,
} from "../domain/contracts";

const CATALOG_ENDPOINT = "/onboarding/catalog/";
const PLANS_ENDPOINT = "/onboarding/plans/";
const REGISTER_ENDPOINT = "/onboarding/register/";
const STATUS_ENDPOINT = "/onboarding/status/";

export async function fetchOrganizationCatalog(): Promise<OrganizationCatalog> {
  const response =
    await apiClient.get<OrganizationCatalog>(
      CATALOG_ENDPOINT,
    );

  return response.data;
}

export async function fetchSaaSPlans(
  organizationType: string,
): Promise<SaaSPlan[]> {
  const params = new URLSearchParams({
    organization_type: organizationType,
  });

  const response =
    await apiClient.get<SaaSPlan[]>(
      `${PLANS_ENDPOINT}?${params.toString()}`,
    );

  return response.data;
}

export async function registerOrganization(
  payload: OrganizationRegistrationPayload,
): Promise<OrganizationOnboardingResult> {
  const response =
    await apiClient.post<OrganizationOnboardingResult>(
      REGISTER_ENDPOINT,
      payload,
    );

  return response.data;
}

export async function fetchOrganizationOnboardingStatus(): Promise<
  OrganizationOnboardingStatusItem[]
> {
  const response =
    await apiClient.get<OrganizationOnboardingStatusItem[]>(
      STATUS_ENDPOINT,
    );

  return response.data;
}

export const onboardingEndpoints = Object.freeze({
  catalog: CATALOG_ENDPOINT,
  plans: PLANS_ENDPOINT,
  register: REGISTER_ENDPOINT,
  status: STATUS_ENDPOINT,
});