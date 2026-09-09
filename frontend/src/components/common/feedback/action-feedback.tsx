/**
 * =============================================================================
 * DatavionOS
 * File:
 * src/components/common/feedback/action-feedback.tsx
 * =============================================================================
 *
 * Reusable contextual action feedback.
 *
 * Feedback from a user action is rendered at the action location rather than
 * through the global toast system.
 * =============================================================================
 */

"use client";

import {
  AlertCircle,
  CheckCircle2,
  Info,
} from "lucide-react";

import { cn } from "@/lib/utils";

export type ActionFeedbackProps =
  Readonly<{
    successMessage?: string | null;

    errorMessage?: string | null;

    infoMessage?: string | null;

    className?: string;
  }>;

export function ActionFeedback({
  successMessage,
  errorMessage,
  infoMessage,
  className,
}: ActionFeedbackProps) {
  if (
    !successMessage &&
    !errorMessage &&
    !infoMessage
  ) {
    return null;
  }

  return (
    <div
      className={cn(
        "mt-3 space-y-2",
        className,
      )}
      aria-live="polite"
    >
      {successMessage && (
        <p
          role="status"
          className="flex items-center justify-end gap-2 text-sm font-medium text-foreground"
        >
          <CheckCircle2
            className="h-4 w-4 shrink-0"
            aria-hidden="true"
          />

          <span>
            {successMessage}
          </span>
        </p>
      )}

      {errorMessage && (
        <p
          role="alert"
          className="flex items-center justify-end gap-2 text-sm font-medium text-destructive"
        >
          <AlertCircle
            className="h-4 w-4 shrink-0"
            aria-hidden="true"
          />

          <span>
            {errorMessage}
          </span>
        </p>
      )}

      {infoMessage && (
        <p
          role="status"
          className="flex items-center justify-end gap-2 text-sm text-muted-foreground"
        >
          <Info
            className="h-4 w-4 shrink-0"
            aria-hidden="true"
          />

          <span>
            {infoMessage}
          </span>
        </p>
      )}
    </div>
  );
}
