/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/organizations/api/mutations.ts
 * =============================================================================
 *
 * Organization mutation definitions.
 * =============================================================================
 */

import {
  mutationOptions,
} from "@tanstack/react-query";

import {
  apiClient,
} from "@/core/api";

import type {
  CreateOrganizationPayload,
  Organization,
  UpdateOrganizationPayload,
} from "../domain";

import {
  organizationEndpoints,
} from "./endpoints";

/**
 * Backend organization detail DTO returned by create/update.
 */
type OrganizationDto = {
  id: string;
  name: string;
  display_name: string;
  code: string;
  slug: string;
  category: string;
  organization_type: string;
  size: string;
  status: string;
  email: string;
  support_email: string;
  phone: string;
  website: string;
  address: string;
  city: string;
  state: string;
  country: string;

  country_ref: string | null;
  region_ref: string | null;
  city_ref: string | null;

  postal_code: string;
  timezone: string;
  registration_number: string;
  tax_number: string;
  license_number: string;
  accreditation: string;
  verification_status: string;
  description: string;
  is_demo: boolean;
  created_at: string;
  updated_at: string;
};

function mapOrganization(
  dto: OrganizationDto,
): Organization {
  return {
    id: dto.id,

    name:
      dto.name,

    displayName:
      dto.display_name,

    code:
      dto.code,

    slug:
      dto.slug,

    category:
      dto.category,

    organizationType:
      dto.organization_type,

    size:
      dto.size,

    status:
      dto.status,

    email:
      dto.email,

    supportEmail:
      dto.support_email,

    phone:
      dto.phone,

    website:
      dto.website,

    address:
      dto.address,

    city:
      dto.city,

    state:
      dto.state,

    country:
      dto.country,

    countryRef:
      dto.country_ref,

    regionRef:
      dto.region_ref,

    cityRef:
      dto.city_ref,

    postalCode:
      dto.postal_code,

    timezone:
      dto.timezone,

    registrationNumber:
      dto.registration_number,

    taxNumber:
      dto.tax_number,

    licenseNumber:
      dto.license_number,

    accreditation:
      dto.accreditation,

    verificationStatus:
      dto.verification_status,

    description:
      dto.description,

    isDemo:
      dto.is_demo,

    createdAt:
      dto.created_at,

    updatedAt:
      dto.updated_at,
  };
}

/**
 * Convert create payload to backend transport contract.
 */
function toCreateApiPayload(
  payload: CreateOrganizationPayload,
) {
  return {
    name:
      payload.name,

    display_name:
      payload.displayName,

    code:
      payload.code,

    slug:
      payload.slug,

    category:
      payload.category,

    organization_type:
      payload.organizationType,

    size:
      payload.size,

    email:
      payload.email,

    support_email:
      payload.supportEmail,

    phone:
      payload.phone,

    website:
      payload.website,

    address:
      payload.address,

    city:
      payload.city,

    state:
      payload.state,

    country:
      payload.country,

    country_ref:
      payload.countryRef,

    region_ref:
      payload.regionRef,

    city_ref:
      payload.cityRef,

    postal_code:
      payload.postalCode,

    timezone:
      payload.timezone,

    registration_number:
      payload.registrationNumber,

    tax_number:
      payload.taxNumber,

    license_number:
      payload.licenseNumber,

    accreditation:
      payload.accreditation,

    description:
      payload.description,

    is_demo:
      payload.isDemo,
  };
}

/**
 * Convert update payload to backend transport contract.
 */
function toUpdateApiPayload(
  payload: UpdateOrganizationPayload,
) {
  return {
    name:
      payload.name,

    display_name:
      payload.displayName,

    category:
      payload.category,

    organization_type:
      payload.organizationType,

    status:
      payload.status,

    size:
      payload.size,

    email:
      payload.email,

    support_email:
      payload.supportEmail,

    phone:
      payload.phone,

    website:
      payload.website,

    address:
      payload.address,

    city:
      payload.city,

    state:
      payload.state,

    country:
      payload.country,

    country_ref:
      payload.countryRef,

    region_ref:
      payload.regionRef,

    city_ref:
      payload.cityRef,

    postal_code:
      payload.postalCode,

    timezone:
      payload.timezone,

    registration_number:
      payload.registrationNumber,

    tax_number:
      payload.taxNumber,

    license_number:
      payload.licenseNumber,

    accreditation:
      payload.accreditation,

    description:
      payload.description,

    is_demo:
      payload.isDemo,
  };
}

async function createOrganization(
  payload: CreateOrganizationPayload,
): Promise<Organization> {
  const response =
    await apiClient.post<OrganizationDto>(
      organizationEndpoints.collection,
      toCreateApiPayload(payload),
    );

  return mapOrganization(
    response.data,
  );
}

async function updateOrganization({
  id,
  payload,
}: {
  id: string;
  payload: UpdateOrganizationPayload;
}): Promise<Organization> {
  const response =
    await apiClient.patch<OrganizationDto>(
      organizationEndpoints.byId(id),
      toUpdateApiPayload(payload),
    );

  return mapOrganization(
    response.data,
  );
}

async function archiveOrganization(
  id: string,
): Promise<void> {
  await apiClient.delete(
    organizationEndpoints.byId(id),
  );
}

export const organizationMutations = {
  create: () =>
    mutationOptions({
      mutationFn:
        createOrganization,
    }),

  update: () =>
    mutationOptions({
      mutationFn:
        updateOrganization,
    }),

  delete: () =>
    mutationOptions({
      mutationFn:
        archiveOrganization,
    }),
} as const;
