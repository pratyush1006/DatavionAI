/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/employees/components/tables/employees-table.tsx
 * =============================================================================
 *
 * Employee data table.
 * =============================================================================
 */

"use client";

import type {
  Employee,
} from "../../domain";

import {
  DataTable,
  DataTableLoading,
  EntityTable,
} from "@/components/common/table";

import {
  employeeColumns,
} from "./employee-columns";

export type EmployeesTableProps =
  Readonly<{
    data: Employee[];

    isLoading?: boolean;
  }>;

export function EmployeesTable({
  data,
  isLoading = false,
}: EmployeesTableProps) {
  return (
    <DataTable>
      {isLoading ? (
        <DataTableLoading />
      ) : (
        <EntityTable
          data={data}
          columns={employeeColumns}
          emptyTitle="No employees found"
          emptyDescription="There are no employees available."
        />
      )}
    </DataTable>
  );
}
