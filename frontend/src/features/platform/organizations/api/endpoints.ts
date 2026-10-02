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

  catalogs: {
    categories: `${BASE_ENDPOINT}catalogs/categories/`,
    types: `${BASE_ENDPOINT}catalogs/types/`,
    sizes: `${BASE_ENDPOINT}catalogs/sizes/`,
  },
} as const;
