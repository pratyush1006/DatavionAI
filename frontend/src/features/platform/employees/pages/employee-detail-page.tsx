/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/employees/pages/employee-detail-page.tsx
 * =============================================================================
 *
 * Employee detail page.
 * =============================================================================
 */

"use client";

import {
  useParams,
} from "next/navigation";

import {
  EmployeeSummaryCard,
} from "../components/cards";

import {
  EditEmployeeDialog,
  EmployeeAssignmentDialog,
  EmployeeContractDialog,
  EmployeeOffboardingDialog,
} from "../components/dialogs";

import {
  EmployeeStatusBadge,
} from "../components/employee-status-badge";
import { EmployeeLifecycleStatusAction } from "../components/employee-lifecycle-status-action";

import {
  useEmployeeQuery,
} from "../hooks";

export function EmployeeDetailPage() {
  const params =
    useParams<{
      employeeId:
        | string
        | string[];
    }>();

  const employeeId =
    Array.isArray(
      params.employeeId,
    )
      ? params.employeeId[0]
      : params.employeeId;

  const {
    data: employee,
    isPending,
    isError,
    error,
  } = useEmployeeQuery(
    employeeId,
  );

  if (isPending) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">
            Employee
          </h1>

          <p className="text-sm text-muted-foreground">
            Loading employee information...
          </p>
        </div>

        <div className="rounded-lg border p-6">
          <p className="text-sm text-muted-foreground">
            Loading employee...
          </p>
        </div>
      </div>
    );
  }

  if (isError || !employee) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">
            Employee
          </h1>

          <p className="text-sm text-muted-foreground">
            Unable to load employee information.
          </p>
        </div>

        <div className="rounded-lg border p-6">
          <p className="text-sm text-destructive">
            {error instanceof Error
              ? error.message
              : "Employee could not be found."}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">
            {employee.fullName}
          </h1>

          <p className="text-sm text-muted-foreground">
            Employee {employee.employeeCode}
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <EmployeeStatusBadge
            status={
              employee.status
            }
          />

          <EmployeeLifecycleStatusAction employee={employee} />

          <EmployeeAssignmentDialog
            employee={employee}
          />

          <EmployeeContractDialog
            employee={employee}
          />

          <EmployeeOffboardingDialog
            employee={employee}
          />

          <EditEmployeeDialog
            employee={employee}
          />
        </div>
      </div>

      <EmployeeSummaryCard
        employee={employee}
      />
    </div>
  );
}
