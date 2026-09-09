/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/employees/domain/constants.ts
 * =============================================================================
 *
 * Employee domain constants.
 *
 * Values are aligned with the backend Employee domain constants.
 * =============================================================================
 */

export const EMPLOYMENT_STATUSES = [
  "DRAFT",
  "ACTIVE",
  "PROBATION",
  "NOTICE_PERIOD",
  "SUSPENDED",
  "TERMINATED",
  "RESIGNED",
  "RETIRED",
] as const;

export type EmploymentStatus =
  (typeof EMPLOYMENT_STATUSES)[number];

export const EMPLOYMENT_TYPES = [
  "FULL_TIME",
  "PART_TIME",
  "CONTRACT",
  "CONSULTANT",
  "INTERN",
  "TEMPORARY",
  "VOLUNTEER",
] as const;

export type EmploymentType =
  (typeof EMPLOYMENT_TYPES)[number];

export const CONTRACT_STATUSES = [
  "DRAFT",
  "ACTIVE",
  "EXPIRED",
  "CANCELLED",
  "RENEWED",
] as const;

export type ContractStatus =
  (typeof CONTRACT_STATUSES)[number];

export const CONTRACT_TYPES = [
  "PERMANENT",
  "FIXED_TERM",
  "TEMPORARY",
  "CONSULTANCY",
] as const;

export type ContractType =
  (typeof CONTRACT_TYPES)[number];

/**
 * Human-readable label helper.
 */
export function formatEmployeeEnumLabel(
  value: string,
): string {
  return value
    .replaceAll("_", " ")
    .toLowerCase()
    .replace(
      /\b\w/g,
      (character) =>
        character.toUpperCase(),
    );
}

/**
 * Select options for employment status.
 */
export const employmentStatusOptions =
  EMPLOYMENT_STATUSES.map((value) => ({
    value,
    label: formatEmployeeEnumLabel(value),
  }));

/**
 * Select options for employment type.
 */
export const employmentTypeOptions =
  EMPLOYMENT_TYPES.map((value) => ({
    value,
    label: formatEmployeeEnumLabel(value),
  }));

/**
 * Select options for contract status.
 */
export const contractStatusOptions =
  CONTRACT_STATUSES.map((value) => ({
    value,
    label: formatEmployeeEnumLabel(value),
  }));

/**
 * Select options for contract type.
 */
export const contractTypeOptions =
  CONTRACT_TYPES.map((value) => ({
    value,
    label: formatEmployeeEnumLabel(value),
  }));
