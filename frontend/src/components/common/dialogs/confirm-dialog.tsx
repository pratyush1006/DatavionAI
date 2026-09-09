/**
 * =============================================================================
 * DatavionOS
 * File: src/components/common/dialogs/confirm-dialog.tsx
 * =============================================================================
 *
 * Reusable confirmation dialog.
 *
 * Responsibilities
 * ----------------
 * - Present a confirmation action.
 * - Handle loading state.
 * - Support contextual success/error/info feedback.
 * - Render action feedback directly below the action buttons.
 *
 * This component is intentionally domain-agnostic so it can be reused for:
 * - Archive
 * - Delete
 * - Restore
 * - Approve
 * - Reject
 * - Activate
 * - Deactivate
 * - Publish
 * - Other contextual confirmation workflows.
 * =============================================================================
 */

"use client";

import type {
  ReactNode,
} from "react";

import {
  AlertTriangle,
} from "lucide-react";

import {
  ActionFeedback,
} from "@/components/common/feedback";

import {
  Button,
} from "@/components/ui/button";

import {
  EntityDialog,
} from "./entity-dialog";

/* =============================================================================
 * Props
 * =============================================================================
 */

export type ConfirmDialogProps =
  Readonly<{
    open: boolean;

    onOpenChange:
      (open: boolean) => void;

    title: string;

    description:
      ReactNode;

    onConfirm:
      () => void | Promise<void>;

    confirmLabel?:
      string;

    cancelLabel?:
      string;

    confirmVariant?:
      | "default"
      | "destructive";

    isLoading?:
      boolean;

    /**
     * Contextual success feedback rendered below the action buttons.
     */
    successMessage?:
      string | null;

    /**
     * Contextual error feedback rendered below the action buttons.
     */
    errorMessage?:
      string | null;

    /**
     * Contextual informational feedback rendered below the action buttons.
     */
    infoMessage?:
      string | null;
  }>;

/* =============================================================================
 * Component
 * =============================================================================
 */

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
  successMessage,
  errorMessage,
  infoMessage,
}: ConfirmDialogProps) {
  return (
    <EntityDialog
      open={open}
      onOpenChange={onOpenChange}
      title={title}
      size="md"
    >
      <div className="flex flex-col gap-6">
        <div className="flex items-start gap-3">
          <AlertTriangle
            className="mt-0.5 size-5 shrink-0 text-destructive"
            aria-hidden="true"
          />

          <div className="text-sm text-muted-foreground">
            {description}
          </div>
        </div>

        <div className="flex flex-col">
          <div className="flex justify-end gap-2">
            <Button
              type="button"
              variant="outline"
              onClick={() =>
                onOpenChange(
                  false,
                )
              }
              disabled={isLoading}
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
              disabled={isLoading}
            >
              {isLoading
                ? "Please wait..."
                : confirmLabel}
            </Button>
          </div>

          <ActionFeedback
            successMessage={
              successMessage
            }
            errorMessage={
              errorMessage
            }
            infoMessage={
              infoMessage
            }
          />
        </div>
      </div>
    </EntityDialog>
  );
}
