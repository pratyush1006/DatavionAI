"use client";

import { useState } from "react";
import { toast } from "sonner";

import { EntityDialog } from "@/components/common/dialogs";
import { Button } from "@/components/ui/button";

import type { Employee } from "../domain";
import {
  useActivateEmployeeMutation,
  useDeactivateEmployeeMutation,
} from "../hooks";

export function EmployeeLifecycleStatusAction({ employee }: { employee: Employee }) {
  const [open, setOpen] = useState(false);
  const activate = useActivateEmployeeMutation();
  const deactivate = useDeactivateEmployeeMutation();
  const isActive = employee.status === "ACTIVE" || employee.status === "PROBATION";
  const mutation = isActive ? deactivate : activate;
  const action = isActive ? "Deactivate" : "Activate";

  async function confirm(): Promise<void> {
    try {
      await mutation.mutateAsync(employee.id);
      toast.success(`${employee.fullName} was ${isActive ? "deactivated" : "activated"}.`);
      setOpen(false);
    } catch (error) {
      toast.error(error instanceof Error ? error.message : `Unable to ${action.toLowerCase()} employee.`);
    }
  }

  return <>
    <Button type="button" variant="outline" onClick={() => setOpen(true)} disabled={employee.isTerminated || mutation.isPending}>
      {action}
    </Button>
    <EntityDialog open={open} onOpenChange={setOpen} title={`${action} employee`} description={`${action} ${employee.fullName}'s employee access. This action is recorded by the backend lifecycle workflow.`} size="sm">
      <div className="flex justify-end gap-3">
        <Button type="button" variant="outline" onClick={() => setOpen(false)} disabled={mutation.isPending}>Cancel</Button>
        <Button type="button" variant={isActive ? "destructive" : "default"} onClick={() => void confirm()} disabled={mutation.isPending}>
          {mutation.isPending ? `${action}ing…` : `${action} employee`}
        </Button>
      </div>
    </EntityDialog>
  </>;
}
