/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/employees/components/dialogs/create-employee-dialog.tsx
 * =============================================================================
 *
 * Create employee dialog.
 * =============================================================================
 */

"use client";

import { useState } from "react";
import { toast } from "sonner";

import {
  EntityDialog,
} from "@/components/common/dialogs";

import {
  Button,
} from "@/components/ui/button";

import type {
  CreateEmployeePayload,
  EmployeeFormValues,
} from "../../domain";

import {
  useCreateEmployeeMutation,
} from "../../hooks";

import {
  EmployeeForm,
} from "../forms";

export function CreateEmployeeDialog() {
  const [open, setOpen] =
    useState(false);

  const mutation =
    useCreateEmployeeMutation();

  async function handleSubmit(
    values: EmployeeFormValues,
  ): Promise<void> {
    try {
      const payload:
        CreateEmployeePayload = {
        organization:
          values.organization,

        user:
          values.user || null,

        employeeCode:
          values.employeeCode
            .trim()
            .toUpperCase(),

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

        joiningDate:
          values.joiningDate,
      };

      await mutation.mutateAsync(
        payload,
      );

      toast.success(
        "Employee created successfully.",
      );

      setOpen(false);
    } catch (error) {
      toast.error(
        error instanceof Error
          ? error.message
          : "Unable to create employee.",
      );
    }
  }

  return (
    <>
      <Button
        type="button"
        onClick={() =>
          setOpen(true)
        }
      >
        Add Employee
      </Button>

      <EntityDialog
        open={open}
        onOpenChange={setOpen}
        title="Create Employee"
        description="Add a new employee to the organization."
        size="xl"
      >
        <EmployeeForm
          isSubmitting={
            mutation.isPending
          }
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
