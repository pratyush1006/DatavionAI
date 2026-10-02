/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/employees/components/dialogs/employee-contract-dialog.tsx
 * =============================================================================
 *
 * Employee contract workflow dialog.
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
  Textarea,
} from "@/components/ui/textarea";

import type {
  Employee,
} from "../../domain";

import {
  useEmployeeContractMutation,
} from "../../hooks";

export type EmployeeContractDialogProps =
  Readonly<{
    employee: Employee;
  }>;

export function EmployeeContractDialog({
  employee,
}: EmployeeContractDialogProps) {
  const [open, setOpen] =
    useState(false);

  const [
    contractData,
    setContractData,
  ] = useState("{}");

  const mutation =
    useEmployeeContractMutation();

  async function handleSubmit(): Promise<void> {
    try {
      const parsed =
        JSON.parse(
          contractData,
        ) as Record<
          string,
          unknown
        >;

      await mutation.mutateAsync({
        id: employee.id,

        payload: {
          contractData: parsed,
        },
      });

      toast.success(
        "Employee contract created successfully.",
      );

      setOpen(false);
    } catch (error) {
      toast.error(
        error instanceof Error
          ? error.message
          : "Unable to create employee contract.",
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
        Contract
      </Button>

      <EntityDialog
        open={open}
        onOpenChange={setOpen}
        title="Employee Contract"
        description={`Create a contract for ${employee.fullName}.`}
        size="lg"
      >
        <div className="space-y-5">
          <Textarea
            value={contractData}
            onChange={(event) =>
              setContractData(
                event.target.value,
              )
            }
            rows={12}
            placeholder='{"contract_type":"PERMANENT","status":"ACTIVE"}'
          />

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
                ? "Creating..."
                : "Create Contract"}
            </Button>
          </div>
        </div>
      </EntityDialog>
    </>
  );
}
