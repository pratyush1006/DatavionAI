/**
 * Organization domain types.
 */

import type {
  OrganizationFormValues,
} from "./schema";

/**
 * Supported organization types.
 */
export const ORGANIZATION_TYPES = [
  "HOSPITAL",
  "CLINIC",
  "LABORATORY",
  "RADIOLOGY",
  "PHARMACY",
  "BLOOD_BANK",
  "CORPORATE",
] as const;

/**
 * Organization type.
 */
export type OrganizationType =
  (typeof ORGANIZATION_TYPES)[number];

/**
 * Organization entity.
 */
export interface Organization {
  id: number;

  uuid?: string;

  name: string;

  code: string;

  organizationType: OrganizationType;

  email: string;

  phone: string;

  address: string;

  city: string;

  state: string;

  country: string;

  isActive: boolean;

  createdAt: string;

  updatedAt: string;
}

/**
 * Payload for creating an organization.
 *
 * Derived from the validated form schema to
 * avoid duplicating field definitions.
 */
export type CreateOrganizationPayload =
  OrganizationFormValues;

/**
 * Payload for updating an organization.
 *
 * Organization code is immutable after creation.
 */
export type UpdateOrganizationPayload =
  Omit<
    OrganizationFormValues,
    "code"
  >;
