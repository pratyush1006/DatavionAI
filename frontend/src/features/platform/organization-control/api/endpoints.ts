// API_CONFIG.baseURL already includes the backend's /api mount point.
const BASE_ENDPOINT = "/organization-control/";

export const organizationControlEndpoints = {
  snapshot: BASE_ENDPOINT,
  moduleToggle: (id: string) =>
    `${BASE_ENDPOINT}modules/${encodeURIComponent(id)}/`,
  featureToggle: (id: string) =>
    `${BASE_ENDPOINT}features/${encodeURIComponent(id)}/`,
} as const;
