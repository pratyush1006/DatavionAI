/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/geography/api/endpoints.ts
 * =============================================================================
 *
 * Canonical Geography API endpoints.
 *
 * Geography is global platform master data.
 * Registration and other domains consume this API but do not own Geography.
 *
 * Backend routes:
 *
 *   GET  /api/geography/countries/
 *   GET  /api/geography/regions/
 *   GET  /api/geography/cities/
 *   POST /api/geography/current-location/
 * =============================================================================
 */

const GEOGRAPHY_BASE = "/geography";

export const geographyEndpoints = {
  countries: `${GEOGRAPHY_BASE}/countries/`,
  regions: `${GEOGRAPHY_BASE}/regions/`,
  cities: `${GEOGRAPHY_BASE}/cities/`,
  currentLocation: `${GEOGRAPHY_BASE}/current-location/`,
} as const;