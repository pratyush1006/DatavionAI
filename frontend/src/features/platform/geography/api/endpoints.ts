/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/geography/api/endpoints.ts
 * =============================================================================
 *
 * Geography API endpoints.
 *
 * Geography is global platform master data and is read-only from the
 * organization UI.
 * =============================================================================
 */

const GEOGRAPHY_BASE = "/geography";

export const geographyEndpoints = {
  countries: `${GEOGRAPHY_BASE}/countries/`,

  regions: `${GEOGRAPHY_BASE}/regions/`,

  cities: `${GEOGRAPHY_BASE}/cities/`,
} as const;
