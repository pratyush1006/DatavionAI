/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/geography/api/keys.ts
 * =============================================================================
 *
 * Geography React Query keys.
 * =============================================================================
 */

export const geographyKeys = {
  all: ["geography"] as const,

  countries: () =>
    [
      ...geographyKeys.all,
      "countries",
    ] as const,

  regions: (
    countryId: string,
  ) =>
    [
      ...geographyKeys.all,
      "regions",
      countryId,
    ] as const,

  cities: (
    regionId: string,
  ) =>
    [
      ...geographyKeys.all,
      "cities",
      regionId,
    ] as const,
} as const;
