/**
 * =============================================================================
 * DatavionOS
 * File:
 * src/features/platform/onboarding/api/index.ts
 * =============================================================================
 *
 * Canonical public API boundary for Organization Onboarding.
 * =============================================================================
 */

export {
  fetchOrganizationCatalog,
  fetchOrganizationOnboardingStatus,
  fetchSaaSPlans,
  onboardingEndpoints,
  registerOrganization,
} from "./onboarding";

export type {
  OrganizationCatalog,
  OrganizationCategoryOption,
  OrganizationOnboardingResult,
  OrganizationOnboardingStatusItem,
  OrganizationRegistrationPayload,
  OrganizationSizeOption,
  OrganizationTypeOption,
  SaaSPlan,
} from "../domain/contracts";
