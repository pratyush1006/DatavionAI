/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/geography/api/queries.ts
 * =============================================================================
 *
 * Geography query definitions.
 *
 * Backend:
 *
 *   GET /api/geography/countries/
 *   GET /api/geography/regions/?country=<uuid>
 *   GET /api/geography/cities/?region=<uuid>
 *
 * Geography is global platform master data.
 *
 * The backend uses the canonical DatavionOS paginated response:
 *
 * {
 *   success: true,
 *   message: "...",
 *   data: [...],
 *   meta: {
 *     pagination: {
 *       count,
 *       page,
 *       page_size,
 *       total_pages,
 *       next,
 *       previous
 *     }
 *   }
 * }
 *
 * The ApiClient preserves `data` and `meta` on ApiSuccessResponse.
 *
 * This module transparently loads all pages because geography dropdowns
 * require complete collections for the selected scope.
 * =============================================================================
 */

import {
  queryOptions,
} from "@tanstack/react-query";

import {
  apiClient,
} from "@/core/api";

import {
  geographyEndpoints,
} from "./endpoints";

import {
  geographyKeys,
} from "./keys";

/* =============================================================================
 * Public DTOs
 * =============================================================================
 */

export interface GeographyCountryDto {
  readonly id: string;
  readonly code: string;
  readonly name: string;
  readonly iso3: string;
  readonly phone_code: string;
  readonly sort_order: number;
  readonly is_active: boolean;
}

export interface GeographyRegionDto {
  readonly id: string;
  readonly country: string;
  readonly code: string;
  readonly name: string;
  readonly region_type: string;
  readonly sort_order: number;
  readonly is_active: boolean;
}

export interface GeographyCityDto {
  readonly id: string;
  readonly country: string;
  readonly region: string | null;
  readonly name: string;
  readonly latitude: string | null;
  readonly longitude: string | null;
  readonly timezone: string;
  readonly sort_order: number;
  readonly is_active: boolean;
}

/* =============================================================================
 * Domain-facing Geography Types
 * =============================================================================
 */

export interface GeographyCountry {
  readonly id: string;
  readonly code: string;
  readonly name: string;
  readonly iso3: string;
  readonly phoneCode: string;
  readonly sortOrder: number;
  readonly isActive: boolean;
}

export interface GeographyRegion {
  readonly id: string;
  readonly countryId: string;
  readonly code: string;
  readonly name: string;
  readonly regionType: string;
  readonly sortOrder: number;
  readonly isActive: boolean;
}

export interface GeographyCity {
  readonly id: string;
  readonly countryId: string;
  readonly regionId: string | null;
  readonly name: string;
  readonly latitude: string | null;
  readonly longitude: string | null;
  readonly timezone: string;
  readonly sortOrder: number;
  readonly isActive: boolean;
}

/* =============================================================================
 * Pagination
 * =============================================================================
 */

interface GeographyPagination {
  readonly count: number;
  readonly page: number;
  readonly page_size: number;
  readonly total_pages: number;
  readonly next: string | null;
  readonly previous: string | null;
}

interface GeographyMeta {
  readonly pagination?: GeographyPagination;
}

/* =============================================================================
 * Query Parameters
 * =============================================================================
 */

const PAGE_SIZE = 100;

interface GeographyQueryParams {
  readonly page?: number;
  readonly page_size?: number;
  readonly country?: string;
  readonly region?: string;
}

/* =============================================================================
 * DTO Mapping
 * =============================================================================
 */

function mapCountry(
  dto: GeographyCountryDto,
): GeographyCountry {
  return {
    id: dto.id,
    code: dto.code,
    name: dto.name,
    iso3: dto.iso3,
    phoneCode: dto.phone_code,
    sortOrder: dto.sort_order,
    isActive: dto.is_active,
  };
}

function mapRegion(
  dto: GeographyRegionDto,
): GeographyRegion {
  return {
    id: dto.id,
    countryId: dto.country,
    code: dto.code,
    name: dto.name,
    regionType: dto.region_type,
    sortOrder: dto.sort_order,
    isActive: dto.is_active,
  };
}

function mapCity(
  dto: GeographyCityDto,
): GeographyCity {
  return {
    id: dto.id,
    countryId: dto.country,
    regionId: dto.region,
    name: dto.name,
    latitude: dto.latitude,
    longitude: dto.longitude,
    timezone: dto.timezone,
    sortOrder: dto.sort_order,
    isActive: dto.is_active,
  };
}

/* =============================================================================
 * Page Fetching
 * =============================================================================
 */

async function fetchPage<T>(
  endpoint: string,
  params: GeographyQueryParams = {},
): Promise<{
  readonly data: T[];
  readonly meta: GeographyMeta | null;
}> {
  const response =
    await apiClient.get<T[]>(
      endpoint,
      {
        params: {
          page_size: PAGE_SIZE,
          ...params,
        },
      },
    );

  return {
    data: Array.isArray(response.data)
      ? response.data
      : [],
    meta:
      response.meta as GeographyMeta | null,
  };
}

/**
 * Fetch every page belonging to a geography collection.
 *
 * Pagination remains a backend responsibility.
 * Consumers receive one complete collection.
 */
async function fetchAllPages<T>(
  endpoint: string,
  params: Omit<
    GeographyQueryParams,
    "page"
  > = {},
): Promise<T[]> {
  const firstPage =
    await fetchPage<T>(
      endpoint,
      {
        ...params,
        page: 1,
      },
    );

  const items = [
    ...firstPage.data,
  ];

  const totalPages =
    firstPage.meta?.pagination
      ?.total_pages ?? 1;

  if (totalPages <= 1) {
    return items;
  }

  for (
    let page = 2;
    page <= totalPages;
    page += 1
  ) {
    const nextPage =
      await fetchPage<T>(
        endpoint,
        {
          ...params,
          page,
        },
      );

    items.push(
      ...nextPage.data,
    );
  }

  return items;
}

/* =============================================================================
 * Countries
 * =============================================================================
 */

async function fetchCountries(): Promise<
  GeographyCountry[]
> {
  const data =
    await fetchAllPages<GeographyCountryDto>(
      geographyEndpoints.countries,
    );

  /*
   * The backend Geography selector already restricts the default response
   * to active records. Do not filter again here.
   *
   * This keeps the frontend transport layer faithful to the backend contract.
   */
  return data.map(
    mapCountry,
  );
}

/* =============================================================================
 * Regions
 * =============================================================================
 */

async function fetchRegions(
  countryId: string,
): Promise<GeographyRegion[]> {
  const data =
    await fetchAllPages<GeographyRegionDto>(
      geographyEndpoints.regions,
      {
        country: countryId,
      },
    );

  /*
   * The backend already applies the active-record policy.
   */
  return data.map(
    mapRegion,
  );
}

/* =============================================================================
 * Cities
 * =============================================================================
 */

async function fetchCities(
  regionId: string,
): Promise<GeographyCity[]> {
  const data =
    await fetchAllPages<GeographyCityDto>(
      geographyEndpoints.cities,
      {
        region: regionId,
      },
    );

  /*
   * The backend already applies the active-record policy.
   */
  return data.map(
    mapCity,
  );
}

/* =============================================================================
 * Query Options
 * =============================================================================
 */

export const geographyQueries = {
  countries: () =>
    queryOptions({
      queryKey:
        geographyKeys.countries(),

      queryFn:
        fetchCountries,

      staleTime:
        1000 * 60 * 60 * 24,

      gcTime:
        1000 * 60 * 60 * 24 * 7,

      refetchOnWindowFocus:
        false,
    }),

  regions: (
    countryId: string,
  ) =>
    queryOptions({
      queryKey:
        geographyKeys.regions(
          countryId,
        ),

      queryFn: () =>
        fetchRegions(
          countryId,
        ),

      enabled:
        countryId.trim().length > 0,

      staleTime:
        1000 * 60 * 60 * 24,

      gcTime:
        1000 * 60 * 60 * 24 * 7,

      refetchOnWindowFocus:
        false,
    }),

  cities: (
    regionId: string,
  ) =>
    queryOptions({
      queryKey:
        geographyKeys.cities(
          regionId,
        ),

      queryFn: () =>
        fetchCities(
          regionId,
        ),

      enabled:
        regionId.trim().length > 0,

      staleTime:
        1000 * 60 * 60 * 24,

      gcTime:
        1000 * 60 * 60 * 24 * 7,

      refetchOnWindowFocus:
        false,
    }),
} as const;
