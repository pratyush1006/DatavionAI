/**
 * =============================================================================
 * DatavionOS
 * File:
 * src/components/common/forms/form-actions.tsx
 * =============================================================================
 *
 * Standard form action buttons with contextual feedback.
 *
 * Action success/error messages are rendered directly below the action buttons.
 * Global toast notifications should not be used for contextual form results.
 * =============================================================================
 */

"use client";

import type { ReactNode } from "react";

import {
  Loader2,
  Save,
  X,
} from "lucide-react";

import { ActionFeedback } from "@/components/common/feedback";

import { Button } from "@/components/ui/button";

import { cn } from "@/lib/utils";

export type FormActionsProps =
  Readonly<{
    isSubmitting?: boolean;

    isEdit?: boolean;

    submitLabel?: string;

    submittingLabel?: string;

    cancelLabel?: string;

    onCancel?: () => void;

    submitIcon?: ReactNode;

    /**
     * Success feedback rendered below the action buttons.
     */
    successMessage?: string | null;

    /**
     * Error feedback rendered below the action buttons.
     */
    errorMessage?: string | null;

    /**
     * Informational feedback rendered below the action buttons.
     */
    infoMessage?: string | null;

    /**
     * Additional content rendered in the action row.
     *
     * Existing consumers use this for validation messages and other
     * contextual content.
     */
    children?: ReactNode;

    className?: string;
  }>;

export function FormActions({
  isSubmitting = false,
  isEdit = false,
  submitLabel,
  submittingLabel,
  cancelLabel = "Cancel",
  onCancel,
  submitIcon,
  successMessage,
  errorMessage,
  infoMessage,
  children,
  className,
}: FormActionsProps) {
  const label =
    submitLabel ??
    (isEdit
      ? "Save Changes"
      : "Create");

  const loadingLabel =
    submittingLabel ??
    (isEdit
      ? "Saving..."
      : "Creating...");

  return (
    <div
      className={cn(
        "border-t pt-6",
        className,
      )}
    >
      <div className="flex items-center justify-end gap-3">
        {children}

        {onCancel && (
          <Button
            type="button"
            variant="outline"
            onClick={onCancel}
            disabled={isSubmitting}
          >
            <X className="mr-2 h-4 w-4" />

            {cancelLabel}
          </Button>
        )}

        <Button
          type="submit"
          disabled={isSubmitting}
        >
          {isSubmitting ? (
            <>
              <Loader2
                className="mr-2 h-4 w-4 animate-spin"
                aria-hidden="true"
              />

              {loadingLabel}
            </>
          ) : (
            <>
              {submitIcon ?? (
                <Save
                  className="mr-2 h-4 w-4"
                  aria-hidden="true"
                />
              )}

              {label}
            </>
          )}
        </Button>
      </div>

      <ActionFeedback
        successMessage={successMessage}
        errorMessage={errorMessage}
        infoMessage={infoMessage}
      />
    </div>
  );
}
