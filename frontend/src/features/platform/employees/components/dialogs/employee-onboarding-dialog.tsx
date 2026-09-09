/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/employees/components/dialogs/employee-onboarding-dialog.tsx
 * =============================================================================
 *
 * Complete employee onboarding workflow dialog.
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

import {
  Textarea,
} from "@/components/ui/textarea";

import {
  useEmployeeOnboardingMutation,
} from "../../hooks";

export function EmployeeOnboardingDialog() {
  const [open, setOpen] =
    useState(false);

  const [
    organizationId,
    setOrganizationId,
  ] = useState("");

  const [
    employeeData,
    setEmployeeData,
  ] = useState("{}");

  const [
    contractData,
    setContractData,
  ] = useState("");

  const [
    assignmentData,
    setAssignmentData,
  ] = useState("");

  const mutation =
    useEmployeeOnboardingMutation();

  function parseOptionalJson(
    value: string,
  ): Record<string, unknown> | null {
    if (!value.trim()) {
      return null;
    }

    return JSON.parse(
      value,
    ) as Record<
      string,
      unknown
    >;
  }

  async function handleSubmit(): Promise<void> {
    try {
      const parsedEmployeeData =
        JSON.parse(
          employeeData,
        ) as Record<
          string,
          unknown
        >;

      const parsedContractData =
        parseOptionalJson(
          contractData,
        );

      const parsedAssignmentData =
        parseOptionalJson(
          assignmentData,
        );

      await mutation.mutateAsync({
        organizationId:
          organizationId.trim(),

        employeeData:
          parsedEmployeeData,

        contractData:
          parsedContractData,

        assignmentData:
          parsedAssignmentData,
      });

      toast.success(
        "Employee onboarding completed successfully.",
      );

      setOpen(false);
    } catch (error) {
      toast.error(
        error instanceof Error
          ? error.message
          : "Unable to complete employee onboarding.",
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
        Onboard Employee
      </Button>

      <EntityDialog
        open={open}
        onOpenChange={setOpen}
        title="Onboard Employee"
        description="Create and complete the employee onboarding workflow."
        size="xl"
      >
        <div className="space-y-5">
          <div className="space-y-2">
            <Label htmlFor="onboarding-organization">
              Organization ID
            </Label>

            <Input
              id="onboarding-organization"
              value={organizationId}
              onChange={(event) =>
                setOrganizationId(
                  event.target.value,
                )
              }
              placeholder="Organization UUID"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="onboarding-employee-data">
              Employee Data
            </Label>

            <Textarea
              id="onboarding-employee-data"
              value={employeeData}
              onChange={(event) =>
                setEmployeeData(
                  event.target.value,
                )
              }
              rows={8}
              placeholder='{"employee_code":"EMP001","designation":"Physician","employment_type":"FULL_TIME","joining_date":"2026-08-31"}'
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="onboarding-contract-data">
              Contract Data
            </Label>

            <Textarea
              id="onboarding-contract-data"
              value={contractData}
              onChange={(event) =>
                setContractData(
                  event.target.value,
                )
              }
              rows={6}
              placeholder='Optional JSON contract payload'
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="onboarding-assignment-data">
              Assignment Data
            </Label>

            <Textarea
              id="onboarding-assignment-data"
              value={assignmentData}
              onChange={(event) =>
                setAssignmentData(
                  event.target.value,
                )
              }
              rows={6}
              placeholder='Optional JSON assignment payload'
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
              onClick={
                handleSubmit
              }
              disabled={
                mutation.isPending ||
                !organizationId.trim()
              }
            >
              {mutation.isPending
                ? "Onboarding..."
                : "Complete Onboarding"}
            </Button>
          </div>
        </div>
      </EntityDialog>
    </>
  );
}
