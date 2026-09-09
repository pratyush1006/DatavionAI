/**
 * =============================================================================
 * DatavionOS
 * File: src/features/clinical/patients/api/keys.ts
 * =============================================================================
 *
 * Canonical TanStack Query keys for Patients.
 * =============================================================================
 */

export const patientKeys = {
  all: ["patients"] as const,

  lists: () =>
    [
      ...patientKeys.all,
      "list",
    ] as const,

  detail: (
    id: string | number,
  ) =>
    [
      ...patientKeys.all,
      "detail",
      String(id),
    ] as const,
} as const;
