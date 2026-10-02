/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/employees/components/dialogs/employee-offboarding-dialog.tsx
 * =============================================================================
 *
 * Employee offboarding workflow dialog.
 * =============================================================================
 */

"use client";

import {
  useState,
} from "react";

import {
  toast,
} from "sonner";

import {
  EntityDialog,
} from "@/components/common/dialogs";

import {
  Button,
} from "@/components/ui/button";

import {
  Input,
} from "@/components/ui/input";

import {
  Label,
} from "@/components/ui/label";

import type {
  Employee,
} from "../../domain";

import {
  useEmployeeOffboardingMutation,
} from "../../hooks";

export type EmployeeOffboardingDialogProps =
  Readonly<{
    employee: Employee;
  }>;

export function EmployeeOffboardingDialog({
  employee,
}: EmployeeOffboardingDialogProps) {
  const [open, setOpen] =
    useState(false);

  const [
    terminationDate,
    setTerminationDate,
  ] = useState("");

  const mutation =
    useEmployeeOffboardingMutation();

  async function handleSubmit(): Promise<void> {
    try {
      await mutation.mutateAsync({
        id: employee.id,

        payload: {
          terminationDate:
            terminationDate ||
            null,
        },
      });

      toast.success(
        "Employee offboarded successfully.",
      );

      setOpen(false);
    } catch (error) {
      toast.error(
        error instanceof Error
          ? error.message
          : "Unable to offboard employee.",
      );
    }
  }

  return (
    <>
      <Button
        type="button"
        variant="outline"
        onClick={() =>
          setOpen(true)
        }
        disabled={
          employee.isTerminated ||
          mutation.isPending
        }
      >
        Offboard
      </Button>

      <EntityDialog
        open={open}
        onOpenChange={setOpen}
        title="Offboard Employee"
        description={`Complete the termination lifecycle for ${employee.fullName}.`}
        size="md"
      >
        <div className="space-y-5">
          <div className="space-y-2">
            <Label htmlFor="employee-termination-date">
              Termination Date
            </Label>

            <Input
              id="employee-termination-date"
              type="date"
              value={terminationDate}
              onChange={(event) =>
                setTerminationDate(
                  event.target.value,
                )
              }
            />
          </div>

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
                handleSubmit
              }
              disabled={
                mutation.isPending
              }
            >
              {mutation.isPending
                ? "Offboarding..."
                : "Offboard Employee"}
            </Button>
          </div>
        </div>
      </EntityDialog>
    </>
  );
}
