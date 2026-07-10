/**
 * Organization query definitions.
 */

import {
  queryOptions,
} from "@tanstack/react-query";

import { apiClient } from "@/core/api";

import type {
  Organization,
  OrganizationType,
} from "../domain";

import {
  organizationEndpoints,
} from "./endpoints";

import {
  organizationKeys,
} from "./keys";

type OrganizationDto = {
  id: number;

  uuid?: string;

  name: string;

  code: string;

  organization_type: string;

  email: string;

  phone: string;

  address: string;

  city: string;

  state: string;

  country: string;

  is_active: boolean;

  created_at: string;

  updated_at: string;
};

type OrganizationListResponse = {
  data: OrganizationDto[];

  meta: {
    pagination: {
      count: number;
      page: number;
      page_size: number;
      total_pages: number;
      next: string | null;
      previous: string | null;
    };
  };
};

function mapOrganization(
  dto: OrganizationDto,
): Organization {
  return {
    id: dto.id,

    uuid: dto.uuid,

    name: dto.name,

    code: dto.code,

    organizationType:
      dto.organization_type.toUpperCase() as OrganizationType,

    email: dto.email,

    phone: dto.phone,

    address: dto.address,

    city: dto.city,

    state: dto.state,

    country: dto.country,

    isActive: dto.is_active,

    createdAt: dto.created_at,

    updatedAt: dto.updated_at,
  };
}

async function fetchOrganizations() {
  const { data } =
    await apiClient.get<OrganizationListResponse>(
      organizationEndpoints.collection,
    );

  return data.data.map(
    mapOrganization,
  );
}

export const organizationQueries = {
  all: () =>
    queryOptions({
      queryKey:
        organizationKeys.lists(),

      queryFn:
        fetchOrganizations,
    }),
} as const;
