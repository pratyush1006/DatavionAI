/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/organizations/domain/types.ts
 * =============================================================================
 *
 * Organization domain contracts.
 * =============================================================================
 */

import type {
  OrganizationFormValues,
  OrganizationUpdateFormValues,
} from "./schema";

/**
 * Organization identifier.
 */
export type OrganizationId = string;

/**
 * Backend organization lifecycle status.
 */
export type OrganizationStatus = string;

/**
 * Backend organization category.
 */
export type OrganizationCategory = string;

/**
 * Backend organization size.
 */
export type OrganizationSize = string;

/**
 * Backend organization type.
 */
export type OrganizationType = string;

/**
 * Organization entity used by the frontend.
 *
 * Geography reference IDs are authoritative identifiers.
 * Legacy country/state/city strings are retained for compatibility and display.
 */
export interface Organization {
  readonly id: OrganizationId;

  readonly name: string;

  readonly displayName: string;

  readonly code: string;

  readonly slug: string;

  readonly category: OrganizationCategory;

  readonly organizationType: OrganizationType;

  readonly size: OrganizationSize;

  readonly status: OrganizationStatus;

  readonly email: string;

  readonly supportEmail: string;

  readonly phone: string;

  readonly website: string;

  readonly address: string;

  readonly city: string;

  readonly state: string;

  readonly country: string;

  readonly countryRef: string | null;

  readonly regionRef: string | null;

  readonly cityRef: string | null;

  readonly postalCode: string;

  readonly timezone: string;

  readonly registrationNumber: string;

  readonly taxNumber: string;

  readonly licenseNumber: string;

  readonly accreditation: string;

  readonly verificationStatus: string;

  readonly description: string;

  readonly isDemo: boolean;

  readonly createdAt: string;

  readonly updatedAt: string;
}

/**
 * Organization collection representation.
 */
export interface OrganizationListItem {
  readonly id: OrganizationId;

  readonly displayName: string;

  readonly code: string;

  readonly category: OrganizationCategory;

  readonly organizationType: OrganizationType;

  readonly status: OrganizationStatus;

  readonly city: string;

  readonly country: string;
}

/**
 * Create payload.
 */
export type CreateOrganizationPayload =
  OrganizationFormValues;

/**
 * Update payload.
 *
 * Code and slug remain immutable after creation.
 */
export type UpdateOrganizationPayload =
  OrganizationUpdateFormValues;
