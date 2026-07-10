/**
 * Reusable confirmation dialog.
 */

"use client";

import type { ReactNode } from "react";

import {
  AlertTriangle,
} from "lucide-react";

import {
  EntityDialog,
} from "./entity-dialog";

import { Button } from "@/components/ui/button";

export type ConfirmDialogProps =
  Readonly<{
    open: boolean;

    onOpenChange: (
      open: boolean,
    ) => void;

    title: string;

    description: ReactNode;

    onConfirm: () => void | Promise<void>;

    confirmLabel?: string;

    cancelLabel?: string;

    confirmVariant?:
      | "default"
      | "destructive";

    isLoading?: boolean;
  }>;

export function ConfirmDialog({
  open,
  onOpenChange,
  title,
  description,
  onConfirm,
  confirmLabel = "Confirm",
  cancelLabel = "Cancel",
  confirmVariant = "destructive",
  isLoading = false,
}: ConfirmDialogProps) {
  return (
    <EntityDialog
      open={open}
      onOpenChange={
        onOpenChange
      }
      title={title}
      description={description}
      size="md"
    >
      <div className="space-y-6">
        <div className="flex items-start gap-3 rounded-lg border border-destructive/20 bg-destructive/5 p-4">
          <AlertTriangle className="mt-0.5 h-5 w-5 shrink-0 text-destructive" />

          <div className="text-sm text-muted-foreground">
            {description}
          </div>
        </div>

        <div className="flex justify-end gap-2">
          <Button
            type="button"
            variant="outline"
            onClick={() =>
              onOpenChange(false)
            }
            disabled={
              isLoading
            }
          >
            {cancelLabel}
          </Button>

          <Button
            type="button"
            variant={
              confirmVariant
            }
            onClick={
              onConfirm
            }
            disabled={
              isLoading
            }
          >
            {isLoading
              ? "Please wait..."
              : confirmLabel}
          </Button>
        </div>
      </div>
    </EntityDialog>
  );
}
