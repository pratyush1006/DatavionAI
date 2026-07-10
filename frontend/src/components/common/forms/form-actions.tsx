/**
 * Standard form action buttons.
 */

"use client";

import type { ReactNode } from "react";

import {
  Loader2,
  Save,
  X,
} from "lucide-react";

import { Button } from "@/components/ui/button";

import { cn } from "@/lib/utils";

export type FormActionsProps = Readonly<{
  isSubmitting?: boolean;

  isEdit?: boolean;

  submitLabel?: string;

  submittingLabel?: string;

  cancelLabel?: string;

  onCancel?: () => void;

  submitIcon?: ReactNode;

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
        "flex items-center justify-end gap-3 border-t pt-6",
        className,
      )}
    >
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
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />

            {loadingLabel}
          </>
        ) : (
          <>
            {submitIcon ?? (
              <Save className="mr-2 h-4 w-4" />
            )}

            {label}
          </>
        )}
      </Button>
    </div>
  );
}
