/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/auth/components/forms/login-actions.tsx
 * =============================================================================
 *
 * Login form actions.
 *
 * Responsibilities
 * ----------------
 * - Render contextual login feedback.
 * - Render the login submit action.
 * - Keep authentication business logic outside the presentation layer.
 *
 * UI hierarchy
 * ------------
 * Contextual feedback is displayed above the primary Sign In action.
 * Success feedback is centered for a clean authentication experience.
 * =============================================================================
 */

"use client";

import {
  Loader2,
  LogIn,
} from "lucide-react";

import {
  ActionFeedback,
} from "@/components/common/feedback";

import {
  Button,
} from "@/components/ui/button";

/* =============================================================================
 * Props
 * =============================================================================
 */

export type LoginActionsProps =
  Readonly<{
    isSubmitting?: boolean;

    successMessage?:
      string | null;

    errorMessage?:
      string | null;

    infoMessage?:
      string | null;
  }>;

/* =============================================================================
 * Component
 * =============================================================================
 */

export function LoginActions({
  isSubmitting = false,
  successMessage,
  errorMessage,
  infoMessage,
}: LoginActionsProps) {
  return (
    <div className="pt-6">
      {successMessage ||
      errorMessage ||
      infoMessage ? (
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
          className="mb-4 mt-0 [&>p]:justify-center"
        />
      ) : null}

      <Button
        type="submit"
        disabled={isSubmitting}
        className="w-full"
      >
        {isSubmitting ? (
          <>
            <Loader2
              className="mr-2 h-4 w-4 animate-spin"
              aria-hidden="true"
            />

            Signing in...
          </>
        ) : (
          <>
            <LogIn
              className="mr-2 h-4 w-4"
              aria-hidden="true"
            />

            Sign In
          </>
        )}
      </Button>
    </div>
  );
}
