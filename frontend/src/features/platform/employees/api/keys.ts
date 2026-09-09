/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/employees/api/keys.ts
 * =============================================================================
 *
 * Employee React Query keys.
 * =============================================================================
 */

export const employeeKeys = {
  all: ["employees"] as const,

  lists: () =>
    [
      ...employeeKeys.all,
      "list",
    ] as const,

  list: (
    params?: Record<string, unknown>,
  ) =>
    [
      ...employeeKeys.lists(),
      params ?? {},
    ] as const,

  details: () =>
    [
      ...employeeKeys.all,
      "detail",
    ] as const,

  detail: (
    id: string,
  ) =>
    [
      ...employeeKeys.details(),
      id,
    ] as const,
} as const;
