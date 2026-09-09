/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/employees/components/dialogs/employee-assignment-dialog.tsx
 * =============================================================================
 *
 * Employee assignment workflow dialog.
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
  useEmployeeAssignmentMutation,
} from "../../hooks";

export type EmployeeAssignmentDialogProps =
  Readonly<{
    employee: Employee;
  }>;

export function EmployeeAssignmentDialog({
  employee,
}: EmployeeAssignmentDialogProps) {
  const [open, setOpen] =
    useState(false);

  const [
    departmentId,
    setDepartmentId,
  ] = useState("");

  const [
    teamId,
    setTeamId,
  ] = useState("");

  const [
    supervisorId,
    setSupervisorId,
  ] = useState("");

  const [
    effectiveFrom,
    setEffectiveFrom,
  ] = useState("");

  const mutation =
    useEmployeeAssignmentMutation();

  async function handleSubmit(): Promise<void> {
    try {
      await mutation.mutateAsync({
        id: employee.id,

        payload: {
          departmentId:
            departmentId.trim() ||
            null,

          teamId:
            teamId.trim() ||
            null,

          supervisorId:
            supervisorId.trim() ||
            null,

          effectiveFrom:
            effectiveFrom ||
            null,
        },
      });

      toast.success(
        "Employee assignment updated successfully.",
      );

      setOpen(false);
    } catch (error) {
      toast.error(
        error instanceof Error
          ? error.message
          : "Unable to update employee assignment.",
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
      >
        Assignment
      </Button>

      <EntityDialog
        open={open}
        onOpenChange={setOpen}
        title="Employee Assignment"
        description={`Update organization structure assignment for ${employee.fullName}.`}
        size="lg"
      >
        <div className="space-y-5">
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="employee-department-id">
                Department ID
              </Label>

              <Input
                id="employee-department-id"
                value={departmentId}
                onChange={(event) =>
                  setDepartmentId(
                    event.target.value,
                  )
                }
                placeholder="Department UUID"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="employee-team-id">
                Team ID
              </Label>

              <Input
                id="employee-team-id"
                value={teamId}
                onChange={(event) =>
                  setTeamId(
                    event.target.value,
                  )
                }
                placeholder="Team UUID"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="employee-supervisor-id">
                Supervisor ID
              </Label>

              <Input
                id="employee-supervisor-id"
                value={supervisorId}
                onChange={(event) =>
                  setSupervisorId(
                    event.target.value,
                  )
                }
                placeholder="Supervisor UUID"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="employee-effective-from">
                Effective From
              </Label>

              <Input
                id="employee-effective-from"
                type="date"
                value={effectiveFrom}
                onChange={(event) =>
                  setEffectiveFrom(
                    event.target.value,
                  )
                }
              />
            </div>
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
              onClick={
                handleSubmit
              }
              disabled={
                mutation.isPending
              }
            >
              {mutation.isPending
                ? "Saving..."
                : "Save Assignment"}
            </Button>
          </div>
        </div>
      </EntityDialog>
    </>
  );
}
