/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/employees/components/dialogs/delete-employee-dialog.tsx
 * =============================================================================
 *
 * Employee deletion dialog.
 *
 * Supports both:
 *
 * 1. Standalone usage with its own trigger.
 * 2. Controlled usage from EmployeeRowActions.
 * =============================================================================
 */

"use client";

import {
  useState,
} from "react";

import {
  Trash2,
} from "lucide-react";

import {
  toast,
} from "sonner";

import {
  EntityDialog,
} from "@/components/common/dialogs";

import {
  Button,
} from "@/components/ui/button";

import type {
  Employee,
} from "../../domain";

import {
  useDeleteEmployeeMutation,
} from "../../hooks";

export type DeleteEmployeeDialogProps =
  Readonly<{
    employee: Employee;

    open?: boolean;

    onOpenChange?: (
      open: boolean,
    ) => void;

    hideTrigger?: boolean;
  }>;

export function DeleteEmployeeDialog({
  employee,
  open: controlledOpen,
  onOpenChange: controlledOnOpenChange,
  hideTrigger = false,
}: DeleteEmployeeDialogProps) {
  const [
    internalOpen,
    setInternalOpen,
  ] = useState(false);

  const mutation =
    useDeleteEmployeeMutation();

  const isControlled =
    controlledOpen !== undefined;

  const open =
    isControlled
      ? controlledOpen
      : internalOpen;

  function setOpen(
    value: boolean,
  ): void {
    if (!isControlled) {
      setInternalOpen(value);
    }

    controlledOnOpenChange?.(
      value,
    );
  }

  async function handleDelete(): Promise<void> {
    try {
      await mutation.mutateAsync(
        employee.id,
      );

      toast.success(
        "Employee deleted successfully.",
      );

      setOpen(false);
    } catch (error) {
      toast.error(
        error instanceof Error
          ? error.message
          : "Unable to delete employee.",
      );
    }
  }

  return (
    <>
      {!hideTrigger && (
        <Button
          type="button"
          variant="ghost"
          size="icon-sm"
          onClick={() =>
            setOpen(true)
          }
          disabled={
            mutation.isPending
          }
          aria-label="Delete employee"
        >
          <Trash2 className="h-4 w-4 text-destructive" />

          <span className="sr-only">
            Delete employee
          </span>
        </Button>
      )}

      <EntityDialog
        open={open}
        onOpenChange={setOpen}
        title="Delete Employee"
        description={`Delete ${employee.fullName} (${employee.employeeCode})? This operation will be processed by the employee lifecycle workflow.`}
        size="md"
      >
        <div className="flex justify-end gap-3">
          <Button
            type="button"
            variant="outline"
            onClick={() =>
              setOpen(false)
            }
            disabled={
              mutation.isPending
            }
          >
            Cancel
          </Button>

          <Button
            type="button"
            variant="destructive"
            onClick={
              handleDelete
            }
            disabled={
              mutation.isPending
            }
          >
            {mutation.isPending
              ? "Deleting..."
              : "Delete Employee"}
          </Button>
        </div>
      </EntityDialog>
    </>
  );
}
