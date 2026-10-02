/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/employees/api/queries.ts
 * =============================================================================
 *
 * Employee query definitions.
 *
 * The canonical ApiClient already validates and unwraps the DatavionOS API
 * envelope. Therefore response.data contains the requested business payload
 * directly.
 * =============================================================================
 */

import {
  queryOptions,
} from "@tanstack/react-query";

import {
  apiClient,
} from "@/core/api";

import type {
  Employee,
  EmployeeManager,
  EmployeeOrganization,
  EmployeeUser,
  EmploymentStatus,
  EmploymentType,
} from "../domain";

import {
  employeeEndpoints,
} from "./endpoints";

import {
  employeeKeys,
} from "./keys";

/**
 * =============================================================================
 * API DTO
 * =============================================================================
 */

type EmployeeDto = {
  id: string;

  organization?: {
    id: string;
    name: string;
    code: string | null;
  } | null;

  user?: {
    id: string;
    email: string;
    name: string;
  } | null;

  employee_code: string;

  full_name: string;

  designation: string;

  work_email: string | null;

  phone_number: string | null;

  employment_type: string;

  status: string;

  joining_date: string;

  confirmation_date: string | null;

  termination_date: string | null;

  manager?: {
    id: string;
    employee_code: string;
    name: string;
  } | null;

  metadata?: Record<
    string,
    unknown
  >;

  is_active_employee: boolean;

  is_terminated: boolean;

  created_at: string;

  updated_at: string;
};

/**
 * =============================================================================
 * DTO Mapping
 * =============================================================================
 */

function mapEmployee(
  dto: EmployeeDto,
): Employee {
  const organization:
    EmployeeOrganization | null =
    dto.organization
      ? {
          id: dto.organization.id,
          name: dto.organization.name,
          code: dto.organization.code,
        }
      : null;

  const user:
    EmployeeUser | null =
    dto.user
      ? {
          id: dto.user.id,
          email: dto.user.email,
          name: dto.user.name,
        }
      : null;

  const manager:
    EmployeeManager | null =
    dto.manager
      ? {
          id: dto.manager.id,
          employeeCode:
            dto.manager.employee_code,
          name:
            dto.manager.name,
        }
      : null;

  return {
    id: dto.id,

    organization,

    user,

    employeeCode:
      dto.employee_code,

    fullName:
      dto.full_name,

    designation:
      dto.designation,

    workEmail:
      dto.work_email,

    phoneNumber:
      dto.phone_number,

    employmentType:
      dto.employment_type.toUpperCase() as EmploymentType,

    status:
      dto.status.toUpperCase() as EmploymentStatus,

    joiningDate:
      dto.joining_date,

    confirmationDate:
      dto.confirmation_date,

    terminationDate:
      dto.termination_date,

    manager,

    metadata:
      dto.metadata ?? {},

    isActiveEmployee:
      dto.is_active_employee,

    isTerminated:
      dto.is_terminated,

    createdAt:
      dto.created_at,

    updatedAt:
      dto.updated_at,
  };
}

/**
 * =============================================================================
 * Fetch Employees
 * =============================================================================
 *
 * ApiClient.get<T>() returns ApiSuccessResponse<T>.
 *
 * The API envelope:
 *
 *     {
 *       success: true,
 *       data: [...]
 *     }
 *
 * is already validated and unwrapped by ApiClient.
 *
 * Therefore:
 *
 *     response.data === EmployeeDto[]
 *
 * NOT:
 *
 *     response.data.data
 */

async function fetchEmployees(): Promise<Employee[]> {
  const response =
    await apiClient.get<EmployeeDto[]>(
      employeeEndpoints.collection,
    );

  return response.data.map(
    mapEmployee,
  );
}

/**
 * =============================================================================
 * Fetch Employee
 * =============================================================================
 */

async function fetchEmployee(
  id: string,
): Promise<Employee> {
  const response =
    await apiClient.get<EmployeeDto>(
      employeeEndpoints.byId(id),
    );

  return mapEmployee(
    response.data,
  );
}

/**
 * =============================================================================
 * Query Definitions
 * =============================================================================
 */

export const employeeQueries = {
  all: () =>
    queryOptions({
      queryKey:
        employeeKeys.lists(),

      queryFn:
        fetchEmployees,
    }),

  detail: (
    id: string,
  ) =>
    queryOptions({
      queryKey:
        employeeKeys.detail(id),

      queryFn: () =>
        fetchEmployee(id),

      enabled:
        id.trim().length > 0,
    }),
} as const;
