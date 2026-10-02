/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/organizations/api/queries.ts
 * =============================================================================
 *
 * Organization query definitions.
 * =============================================================================
 */

import {
  queryOptions,
} from "@tanstack/react-query";

import {
  apiClient,
} from "@/core/api";

import type {
  Organization,
  OrganizationListItem,
} from "../domain";

import {
  organizationEndpoints,
} from "./endpoints";

import {
  organizationKeys,
} from "./keys";

/**
 * Backend organization collection DTO.
 */
type OrganizationListDto = {
  id: string;
  name: string;
  display_name: string;
  code: string;
  category: string;
  organization_type: string;
  status: string;
  city: string;
  country: string;
};

/**
 * Backend organization detail DTO.
 */
type OrganizationDetailDto =
  OrganizationListDto & {
    name: string;
    slug: string;
    size: string;
    email: string;
    support_email: string;
    phone: string;
    website: string;
    address: string;
    state: string;

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

type OrganizationListResponse =
  OrganizationListDto[];

type OrganizationDetailResponse =
  OrganizationDetailDto;

export type OrganizationCatalogOption = {
  readonly value: string;
  readonly label: string;
};

type OrganizationCatalogDto = {
  id: string;
  name: string;
  code: string;
};

function mapOrganizationListItem(
  dto: OrganizationListDto,
): OrganizationListItem {
  return {
    id: dto.id,

    displayName:
      dto.display_name || dto.name,

    code:
      dto.code,

    category:
      dto.category,

    organizationType:
      dto.organization_type,

    status:
      dto.status,

    city:
      dto.city,

    country:
      dto.country,
  };
}

function mapOrganizationDetail(
  dto: OrganizationDetailDto,
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

async function fetchOrganizations():
  Promise<OrganizationListItem[]> {
  const response =
    await apiClient.get<
      OrganizationListResponse
    >(
      organizationEndpoints.collection,
    );

  return response.data.map(
    mapOrganizationListItem,
  );
}

async function fetchOrganization(
  id: string,
): Promise<Organization> {
  const response =
    await apiClient.get<
      OrganizationDetailResponse
    >(
      organizationEndpoints.byId(id),
    );

  return mapOrganizationDetail(
    response.data,
  );
}

async function fetchCatalog(
  endpoint: string,
): Promise<OrganizationCatalogOption[]> {
  const response = await apiClient.get<OrganizationCatalogDto[]>(endpoint);
  return response.data.map((item) => ({
    value: item.code || item.id,
    label: item.name,
  }));
}

export const organizationQueries = {
  all: () =>
    queryOptions({
      queryKey:
        organizationKeys.lists(),

      queryFn:
        fetchOrganizations,
    }),

  detail: (
    id: string,
    enabled = true,
  ) =>
    queryOptions({
      queryKey:
        organizationKeys.detail(id),

      queryFn: () =>
        fetchOrganization(id),

      enabled:
        enabled &&
        id.trim().length > 0,
    }),

  categories: () => queryOptions({
    queryKey: [...organizationKeys.catalogs(), "categories"],
    queryFn: () => fetchCatalog(organizationEndpoints.catalogs.categories),
    staleTime: 15 * 60_000,
  }),

  types: () => queryOptions({
    queryKey: [...organizationKeys.catalogs(), "types"],
    queryFn: () => fetchCatalog(organizationEndpoints.catalogs.types),
    staleTime: 15 * 60_000,
  }),

  sizes: () => queryOptions({
    queryKey: [...organizationKeys.catalogs(), "sizes"],
    queryFn: () => fetchCatalog(organizationEndpoints.catalogs.sizes),
    staleTime: 15 * 60_000,
  }),
} as const;
