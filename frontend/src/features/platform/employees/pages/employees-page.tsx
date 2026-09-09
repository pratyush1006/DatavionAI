/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/employees/pages/employees-page.tsx
 * =============================================================================
 *
 * Employee listing page.
 * =============================================================================
 */

"use client";

import {
  ListPage,
} from "@/components/common/page";

import {
  CreateEmployeeDialog,
  EmployeeOnboardingDialog,
} from "../components/dialogs";

import {
  EmployeesTable,
} from "../components/tables";

import {
  useEmployeesQuery,
} from "../hooks";

export function EmployeesPage() {
  const {
    data = [],
    isPending,
  } = useEmployeesQuery();

  return (
    <ListPage
      title="Employees"
      description="Manage employees and their employment lifecycle across the organization."
      actions={
        <div className="flex items-center gap-2">
          <EmployeeOnboardingDialog />
          <CreateEmployeeDialog />
        </div>
      }
    >
      <EmployeesTable
        data={data}
        isLoading={isPending}
      />
    </ListPage>
  );
}
