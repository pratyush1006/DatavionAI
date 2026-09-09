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
    id: string,
  ) =>
    `${BASE_ENDPOINT}${encodeURIComponent(id)}/`,
} as const;
