/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/employees/api/endpoints.ts
 * =============================================================================
 *
 * Employee API endpoints.
 *
 * Routes are aligned with:
 *
 * apps/organization/employees/api/urls.py
 * =============================================================================
 */

const BASE_ENDPOINT = "/employees/";

export const employeeEndpoints = {
  base: BASE_ENDPOINT,

  collection: BASE_ENDPOINT,

  byId: (
    id: string,
  ) => `${BASE_ENDPOINT}${id}/`,

  activate: (
    id: string,
  ) => `${BASE_ENDPOINT}${id}/activate/`,

  deactivate: (
    id: string,
  ) => `${BASE_ENDPOINT}${id}/deactivate/`,

  assignment: (
    id: string,
  ) => `${BASE_ENDPOINT}${id}/assignment/`,

  contract: (
    id: string,
  ) => `${BASE_ENDPOINT}${id}/contract/`,

  offboard: (
    id: string,
  ) => `${BASE_ENDPOINT}${id}/offboard/`,

  onboard:
    `${BASE_ENDPOINT}onboard/`,
} as const;
