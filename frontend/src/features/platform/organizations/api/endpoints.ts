/**
 * Organization API endpoints.
 */

const BASE_ENDPOINT =
  "/organizations/";

export const organizationEndpoints = {
  base: BASE_ENDPOINT,

  collection:
    BASE_ENDPOINT,

  byId: (
    id: number | string,
  ) => `${BASE_ENDPOINT}${id}/`,
} as const;
