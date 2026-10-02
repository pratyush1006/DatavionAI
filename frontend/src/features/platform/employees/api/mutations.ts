/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/employees/api/mutations.ts
 * =============================================================================
 *
 * Employee mutation definitions.
 *
 * CRUD and lifecycle operations intentionally remain separate because the
 * backend exposes them as separate workflows.
 * =============================================================================
 */

import {
  mutationOptions,
} from "@tanstack/react-query";

import {
  apiClient,
} from "@/core/api";

import type {
  CreateEmployeePayload,
  Employee,
  EmployeeAssignmentPayload,
  EmployeeContractPayload,
  EmployeeLifecycleResult,
  EmployeeOffboardingPayload,
  EmployeeOnboardingPayload,
  UpdateEmployeePayload,
} from "../domain";

import {
  employeeEndpoints,
} from "./endpoints";

type LifecycleDto = {
  employee_id: string;

  event_id?: string | null;

  activated?: boolean;

  deactivated?: boolean;

  offboarded?: boolean;
};

function mapLifecycleResult(
  data: LifecycleDto,
): EmployeeLifecycleResult {
  return {
    employeeId:
      data.employee_id,

    eventId:
      data.event_id ?? null,

    activated:
      data.activated,

    deactivated:
      data.deactivated,

    offboarded:
      data.offboarded,
  };
}

async function createEmployee(
  payload: CreateEmployeePayload,
): Promise<Employee> {
  const response =
    await apiClient.post<Employee>(
      employeeEndpoints.collection,
      {
        organization:
          payload.organization,

        user:
          payload.user || null,

        employee_code:
          payload.employeeCode,

        designation:
          payload.designation,

        work_email:
          payload.workEmail || null,

        phone_number:
          payload.phoneNumber || null,

        employment_type:
          payload.employmentType,

        joining_date:
          payload.joiningDate,
      },
    );

  return response.data;
}

async function updateEmployee({
  id,
  payload,
}: {
  id: string;

  payload:
    UpdateEmployeePayload;
}): Promise<Employee> {
  const response =
    await apiClient.patch<Employee>(
      employeeEndpoints.byId(id),
      {
        designation:
          payload.designation,

        work_email:
          payload.workEmail || null,

        phone_number:
          payload.phoneNumber || null,

        employment_type:
          payload.employmentType,

        confirmation_date:
          payload.confirmationDate ||
          null,

        metadata:
          payload.metadata,
      },
    );

  return response.data;
}

async function deleteEmployee(
  id: string,
): Promise<void> {
  await apiClient.delete(
    employeeEndpoints.byId(id),
  );
}

async function activateEmployee(
  id: string,
): Promise<EmployeeLifecycleResult> {
  const response =
    await apiClient.post<LifecycleDto>(
      employeeEndpoints.activate(id),
    );

  return mapLifecycleResult(
    response.data,
  );
}

async function deactivateEmployee(
  id: string,
): Promise<EmployeeLifecycleResult> {
  const response =
    await apiClient.post<LifecycleDto>(
      employeeEndpoints.deactivate(id),
    );

  return mapLifecycleResult(
    response.data,
  );
}

async function assignEmployee({
  id,
  payload,
}: {
  id: string;

  payload:
    EmployeeAssignmentPayload;
}): Promise<EmployeeLifecycleResult> {
  const response =
    await apiClient.post<LifecycleDto>(
      employeeEndpoints.assignment(id),
      {
        department_id:
          payload.departmentId ??
          null,

        team_id:
          payload.teamId ??
          null,

        supervisor_id:
          payload.supervisorId ??
          null,

        effective_from:
          payload.effectiveFrom ??
          null,
      },
    );

  return mapLifecycleResult(
    response.data,
  );
}

async function createEmployeeContract({
  id,
  payload,
}: {
  id: string;

  payload:
    EmployeeContractPayload;
}): Promise<EmployeeLifecycleResult> {
  const response =
    await apiClient.post<LifecycleDto>(
      employeeEndpoints.contract(id),
      {
        contract_data:
          payload.contractData,
      },
    );

  return mapLifecycleResult(
    response.data,
  );
}

async function onboardEmployee(
  payload:
    EmployeeOnboardingPayload,
): Promise<EmployeeLifecycleResult> {
  const response =
    await apiClient.post<LifecycleDto>(
      employeeEndpoints.onboard,
      {
        organization_id:
          payload.organizationId,

        employee_data:
          payload.employeeData,

        contract_data:
          payload.contractData ??
          null,

        assignment_data:
          payload.assignmentData ??
          null,
      },
    );

  return mapLifecycleResult(
    response.data,
  );
}

async function offboardEmployee({
  id,
  payload,
}: {
  id: string;

  payload:
    EmployeeOffboardingPayload;
}): Promise<EmployeeLifecycleResult> {
  const response =
    await apiClient.post<LifecycleDto>(
      employeeEndpoints.offboard(id),
      {
        termination_date:
          payload.terminationDate ??
          null,
      },
    );

  return mapLifecycleResult(
    response.data,
  );
}

export const employeeMutations = {
  create: () =>
    mutationOptions({
      mutationFn:
        createEmployee,
    }),

  update: () =>
    mutationOptions({
      mutationFn:
        updateEmployee,
    }),

  delete: () =>
    mutationOptions({
      mutationFn:
        deleteEmployee,
    }),

  activate: () =>
    mutationOptions({
      mutationFn:
        activateEmployee,
    }),

  deactivate: () =>
    mutationOptions({
      mutationFn:
        deactivateEmployee,
    }),

  assignment: () =>
    mutationOptions({
      mutationFn:
        assignEmployee,
    }),

  contract: () =>
    mutationOptions({
      mutationFn:
        createEmployeeContract,
    }),

  onboard: () =>
    mutationOptions({
      mutationFn:
        onboardEmployee,
    }),

  offboard: () =>
    mutationOptions({
      mutationFn:
        offboardEmployee,
    }),
} as const;
