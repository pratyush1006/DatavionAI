/**
 * =============================================================================
 * DatavionOS
 * File: src/features/clinical/patients/api/endpoints.ts
 * =============================================================================
 *
 * Patient API endpoint definitions.
 * =============================================================================
 */

export const patientEndpoints = {
  collection: "/patient-management/patients/",

  byId: (
    id: string | number,
  ) =>
    `/patients/${String(id)}/`,
} as const;
