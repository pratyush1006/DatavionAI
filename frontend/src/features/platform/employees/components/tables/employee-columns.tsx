/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/employees/components/tables/employee-columns.tsx
 * =============================================================================
 *
 * Employee table columns.
 * =============================================================================
 */

"use client";

import type {
  ColumnDef,
} from "@tanstack/react-table";

import {
  BriefcaseBusiness,
  Mail,
  Phone,
  UserRound,
} from "lucide-react";

import type {
  Employee,
} from "../../domain";

import {
  EmployeeStatusBadge,
} from "../employee-status-badge";

import {
  EmployeeRowActions,
} from "./employee-row-actions";

export const employeeColumns:
  ColumnDef<Employee>[] = [
    {
      accessorKey: "fullName",

      header: "Employee",

      cell: ({ row }) => {
        const employee = row.original;

        return (
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-primary/10">
              <UserRound className="h-5 w-5 text-primary" />
            </div>

            <div className="min-w-0">
              <div className="truncate font-medium">
                {employee.fullName}
              </div>

              <div className="text-xs text-muted-foreground">
                {employee.employeeCode}
              </div>
            </div>
          </div>
        );
      },
    },

    {
      accessorKey: "designation",

      header: "Designation",

      cell: ({ row }) => (
        <div className="flex items-center gap-2">
          <BriefcaseBusiness className="h-4 w-4 text-muted-foreground" />

          <span>
            {row.original.designation ||
              "Not specified"}
          </span>
        </div>
      ),
    },

    {
      accessorKey: "employmentType",

      header: "Employment",

      cell: ({ row }) => (
        <div className="text-sm">
          {row.original.employmentType.replaceAll(
            "_",
            " ",
          )}
        </div>
      ),
    },

    {
      id: "contact",

      header: "Contact",

      cell: ({ row }) => {
        const employee = row.original;

        return (
          <div>
            <div className="flex items-center gap-2">
              <Mail className="h-3.5 w-3.5 text-muted-foreground" />

              <span className="truncate">
                {employee.workEmail || "—"}
              </span>
            </div>

            <div className="mt-1 flex items-center gap-2 text-xs text-muted-foreground">
              <Phone className="h-3.5 w-3.5" />

              <span>
                {employee.phoneNumber || "—"}
              </span>
            </div>
          </div>
        );
      },
    },

    {
      accessorKey: "status",

      header: "Status",

      cell: ({ row }) => (
        <EmployeeStatusBadge
          status={row.original.status}
        />
      ),
    },

    {
      id: "actions",

      header: "",

      enableSorting: false,

      enableHiding: false,

      cell: ({ row }) => (
        <EmployeeRowActions
          employee={row.original}
        />
      ),
    },
  ];
