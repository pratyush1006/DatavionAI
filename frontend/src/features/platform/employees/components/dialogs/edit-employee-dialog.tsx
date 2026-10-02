/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/employees/components/dialogs/edit-employee-dialog.tsx
 * =============================================================================
 *
 * Edit employee dialog.
 *
 * Supports both:
 *
 * 1. Standalone usage with its own trigger.
 * 2. Controlled usage from EmployeeRowActions.
 *
 * Immutable creation fields such as organization, user, employee code and
 * joining date are displayed but are not submitted as update fields.
 * =============================================================================
 */

"use client";

import {
  useState,
} from "react";

import {
  Pencil,
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
  EmployeeFormValues,
  UpdateEmployeePayload,
} from "../../domain";

import {
  useUpdateEmployeeMutation,
} from "../../hooks";

import {
  EmployeeForm,
} from "../forms";

export type EditEmployeeDialogProps =
  Readonly<{
    employee: Employee;

    open?: boolean;

    onOpenChange?: (
      open: boolean,
    ) => void;

    hideTrigger?: boolean;
  }>;

export function EditEmployeeDialog({
  employee,
  open: controlledOpen,
  onOpenChange: controlledOnOpenChange,
  hideTrigger = false,
}: EditEmployeeDialogProps) {
  const [
    internalOpen,
    setInternalOpen,
  ] = useState(false);

  const mutation =
    useUpdateEmployeeMutation();

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

  async function handleSubmit(
    values: EmployeeFormValues,
  ): Promise<void> {
    try {
      const payload:
        UpdateEmployeePayload = {
        designation:
          values.designation.trim(),

        workEmail:
          values.workEmail?.trim() ||
          null,

        phoneNumber:
          values.phoneNumber?.trim() ||
          null,

        employmentType:
          values.employmentType,

        confirmationDate:
          null,

        metadata: {},
      };

      await mutation.mutateAsync({
        id: employee.id,
        payload,
      });

      toast.success(
        "Employee updated successfully.",
      );

      setOpen(false);
    } catch (error) {
      toast.error(
        error instanceof Error
          ? error.message
          : "Unable to update employee.",
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
          aria-label="Edit employee"
        >
          <Pencil className="h-4 w-4" />

          <span className="sr-only">
            Edit employee
          </span>
        </Button>
      )}

      <EntityDialog
        open={open}
        onOpenChange={setOpen}
        title="Edit Employee"
        description="Update employee employment and contact information."
        size="xl"
      >
        <EmployeeForm
          defaultValues={{
            organization:
              employee.organization
                ?.id ?? "",

            user:
              employee.user?.id ?? "",

            employeeCode:
              employee.employeeCode,

            designation:
              employee.designation,

            workEmail:
              employee.workEmail ?? "",

            phoneNumber:
              employee.phoneNumber ?? "",

            employmentType:
              employee.employmentType,

            joiningDate:
              employee.joiningDate,
          }}
          isSubmitting={
            mutation.isPending
          }
          isEdit
          onSubmit={
            handleSubmit
          }
          onCancel={() =>
            setOpen(false)
          }
        />
      </EntityDialog>
    </>
  );
}
