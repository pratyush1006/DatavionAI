/**
 * ----------------------------------------------------------------------
 * Delete Dialog
 * ----------------------------------------------------------------------
 *
 * Purpose:
 * Enterprise confirmation dialog for destructive actions.
 *
 * Used By:
 * - Organizations
 * - Departments
 * - Teams
 * - Users
 * - Patients
 * - Laboratories
 * - Billing
 *
 * ----------------------------------------------------------------------
 */

"use client";

import {
  AlertTriangle,
} from "lucide-react";

import { Button } from "@/components/ui/button";

import {
  EntityDialog,
} from "./entity-dialog";

export type DeleteDialogProps = Readonly<{
  open: boolean;

  onOpenChange: (
    open: boolean,
  ) => void;

  title?: string;

  description?: string;

  confirmLabel?: string;

  cancelLabel?: string;

  isDeleting?: boolean;

  onConfirm: () => void | Promise<void>;
}>;

export function DeleteDialog({
  open,
  onOpenChange,
  title = "Delete Record",
  description = "This action cannot be undone. Are you sure you want to continue?",
  confirmLabel = "Delete",
  cancelLabel = "Cancel",
  isDeleting = false,
  onConfirm,
}: DeleteDialogProps) {
  return (
    <EntityDialog
      open={open}
      onOpenChange={onOpenChange}
      title={title}
      description={description}
      size="sm"
      footer={
        <div className="flex justify-end gap-2">
          <Button
            variant="outline"
            onClick={() => onOpenChange(false)}
            disabled={isDeleting}
          >
            {cancelLabel}
          </Button>

          <Button
            variant="destructive"
            onClick={onConfirm}
            disabled={isDeleting}
          >
            {isDeleting
              ? "Deleting..."
              : confirmLabel}
          </Button>
        </div>
      }
    >
      <div className="flex items-start gap-4">
        <div className="rounded-full bg-destructive/10 p-3">
          <AlertTriangle className="h-6 w-6 text-destructive" />
        </div>

        <div className="space-y-2">
          <h3 className="font-semibold">
            Please Confirm
          </h3>

          <p className="text-sm text-muted-foreground">
            Once deleted, this data cannot be
            recovered.
          </p>
        </div>
      </div>
    </EntityDialog>
  );
}
