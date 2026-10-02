"use client";

import { apiPublicGet, apiPublicRequest } from "@/lib/backend/http";
import { ENDPOINTS } from "@/lib/backend/endpoints";
import type { CurrentLocationResult } from "@/lib/backend/contracts";

export type CatalogOption = {
  id: string;
  name: string;
  code?: string;
  category?: string | null;
};

export type OrganizationCatalog = {
  categories: CatalogOption[];
  types: CatalogOption[];
  sizes: CatalogOption[];
};

type OrganizationCatalogRecord = {
  code: string;
  name: string;
  category?: string | null;
};

export type GeographyOption = CatalogOption & {
  country?: string;
  region?: string;
  timezone?: string | null;
};

async function getJson<T>(path: string): Promise<T> {
  const response = await apiPublicGet<T>(path);
  return response.data;
}

export async function getOrganizationCatalog(): Promise<OrganizationCatalog> {
  const catalog = await getJson<{
    categories: OrganizationCatalogRecord[];
    types: OrganizationCatalogRecord[];
    sizes: OrganizationCatalogRecord[];
  }>(
    ENDPOINTS.onboarding.catalog,
  );

  const normalize = (
    items: OrganizationCatalogRecord[],
  ): CatalogOption[] =>
    items.map((item) => ({
      id: item.code,
      code: item.code,
      name: item.name,
      category: item.category,
    }));

  return {
    categories: normalize(catalog.categories),
    types: normalize(catalog.types),
    sizes: normalize(catalog.sizes),
  };
}

export async function getOrganizationTypes(): Promise<CatalogOption[]> {
  return (await getOrganizationCatalog()).types;
}

export async function getOrganizationCategories(): Promise<CatalogOption[]> {
  return (await getOrganizationCatalog()).categories;
}

export async function getOrganizationSizes(): Promise<CatalogOption[]> {
  return (await getOrganizationCatalog()).sizes;
}

export async function getCountries(): Promise<
  GeographyOption[]
> {
  return getJson<GeographyOption[]>(ENDPOINTS.geography.countries);
}

export async function getStates(
  countryId: string,
): Promise<GeographyOption[]> {
  return getJson<GeographyOption[]>(
    `${ENDPOINTS.geography.regions}?country=${encodeURIComponent(countryId)}`,
  );
}

export async function getCities(
  regionId: string,
): Promise<GeographyOption[]> {
  return getJson<GeographyOption[]>(
    `${ENDPOINTS.geography.cities}?region=${encodeURIComponent(regionId)}`,
  );
}

export async function resolveCurrentLocation(
  latitude: number,
  longitude: number,
  accuracyMeters?: number | null,
): Promise<CurrentLocationResult> {
  return apiPublicRequest<CurrentLocationResult>(
    ENDPOINTS.geography.currentLocation,
    {
      method: "POST",
      body: JSON.stringify({
        latitude,
        longitude,
        accuracy_meters: accuracyMeters ?? null,
      }),
    },
  );
}
