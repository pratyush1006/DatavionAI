/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/employees/components/tables/employee-row-actions.tsx
 * =============================================================================
 *
 * Employee row actions.
 *
 * The row action menu owns the action state and opens the corresponding
 * employee lifecycle dialogs.
 * =============================================================================
 */

"use client";

import {
  useState,
} from "react";

import {
  MoreHorizontal,
} from "lucide-react";

import {
  Button,
} from "@/components/ui/button";

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

import type {
  Employee,
} from "../../domain";

import {
  DeleteEmployeeDialog,
  EditEmployeeDialog,
} from "../dialogs";

export type EmployeeRowActionsProps =
  Readonly<{
    employee: Employee;

    onView?: (
      employee: Employee,
    ) => void;
  }>;

export function EmployeeRowActions({
  employee,
  onView,
}: EmployeeRowActionsProps) {
  const [editOpen, setEditOpen] =
    useState(false);

  const [deleteOpen, setDeleteOpen] =
    useState(false);

  function handleView(): void {
    onView?.(employee);
  }

  function handleEdit(): void {
    setEditOpen(true);
  }

  function handleDelete(): void {
    setDeleteOpen(true);
  }

  return (
    <>
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button
            type="button"
            variant="ghost"
            size="icon-sm"
            aria-label={`Actions for ${employee.fullName}`}
          >
            <MoreHorizontal className="h-4 w-4" />

            <span className="sr-only">
              Employee actions
            </span>
          </Button>
        </DropdownMenuTrigger>

        <DropdownMenuContent
          align="end"
          className="w-48"
        >
          {onView && (
            <DropdownMenuItem
              onSelect={handleView}
            >
              View Employee
            </DropdownMenuItem>
          )}

          <DropdownMenuItem
            onSelect={handleEdit}
          >
            Edit Employee
          </DropdownMenuItem>

          <DropdownMenuSeparator />

          <DropdownMenuItem
            onSelect={handleDelete}
            className="text-destructive focus:text-destructive"
          >
            Delete Employee
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>

      <EditEmployeeDialog
        employee={employee}
        open={editOpen}
        onOpenChange={setEditOpen}
      />

      <DeleteEmployeeDialog
        employee={employee}
        open={deleteOpen}
        onOpenChange={setDeleteOpen}
      />
    </>
  );
}
