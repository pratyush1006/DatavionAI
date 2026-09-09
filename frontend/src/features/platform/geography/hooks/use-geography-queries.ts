/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/geography/hooks/use-geography-queries.ts
 * =============================================================================
 *
 * Geography query hooks.
 * =============================================================================
 */

"use client";

import {
  useQuery,
} from "@tanstack/react-query";

import {
  geographyQueries,
} from "../api";

/**
 * Load all active countries.
 */
export function useCountriesQuery() {
  return useQuery(
    geographyQueries.countries(),
  );
}

/**
 * Load active regions for a country.
 */
export function useRegionsQuery(
  countryId: string,
) {
  return useQuery(
    geographyQueries.regions(
      countryId,
    ),
  );
}

/**
 * Load active cities for a region.
 */
export function useCitiesQuery(
  regionId: string,
) {
  return useQuery(
    geographyQueries.cities(
      regionId,
    ),
  );
}
