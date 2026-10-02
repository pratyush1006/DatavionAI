/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/auth/components/forms/reset-password-form.tsx
 * =============================================================================
 *
 * Password-reset completion form.
 *
 * Responsibilities
 * ----------------
 * - Collect the password-reset OTP.
 * - Collect the new password.
 * - Validate password confirmation.
 * - Delegate submission to the page layer.
 * - Render contextual reset feedback below the action.
 *
 * This component performs no API calls and contains no authentication
 * business logic.
 * =============================================================================
 */

"use client";

import {
  zodResolver,
} from "@hookform/resolvers/zod";

import {
  useForm,
} from "react-hook-form";

import {
  ActionFeedback,
} from "@/components/common/feedback";

import {
  AppForm,
} from "@/components/common/forms/app-form";

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
  resetPasswordDefaults,
} from "../../domain/defaults";

import {
  resetPasswordSchema,
  type ResetPasswordFormValues,
} from "../../domain/schema";

/* =============================================================================
 * Props
 * =============================================================================
 */

export type ResetPasswordFormProps =
  Readonly<{
    isSubmitting?: boolean;

    successMessage?:
      string | null;

    errorMessage?:
      string | null;

    infoMessage?:
      string | null;

    onSubmit: (
      values: ResetPasswordFormValues,
    ) => void | Promise<void>;
  }>;

/* =============================================================================
 * Component
 * =============================================================================
 */

export function ResetPasswordForm({
  isSubmitting = false,
  successMessage,
  errorMessage,
  infoMessage,
  onSubmit,
}: ResetPasswordFormProps) {
  const form =
    useForm<ResetPasswordFormValues>({
      resolver:
        zodResolver(
          resetPasswordSchema,
        ),

      defaultValues:
        resetPasswordDefaults,

      mode: "onBlur",
    });

  return (
    <AppForm
      onSubmit={form.handleSubmit(
        onSubmit,
      )}
    >
      <div className="space-y-2">
        <Label htmlFor="reset-password-otp">
          Verification code
        </Label>

        <Input
          id="reset-password-otp"
          type="text"
          inputMode="numeric"
          autoComplete="one-time-code"
          maxLength={6}
          placeholder="Enter 6-digit code"
          disabled={
            isSubmitting
          }
          {...form.register(
            "otp",
            {
              onChange: (
                event,
              ) => {
                event.target.value =
                  event.target.value
                    .replace(
                      /\D/g,
                      "",
                    )
                    .slice(
                      0,
                      6,
                    );
              },
            },
          )}
        />

        {form.formState.errors.otp ? (
          <p className="text-sm text-destructive">
            {
              form.formState.errors
                .otp.message
            }
          </p>
        ) : null}
      </div>

      <div className="space-y-2">
        <Label htmlFor="reset-password-new">
          New password
        </Label>

        <Input
          id="reset-password-new"
          type="password"
          autoComplete="new-password"
          placeholder="Enter your new password"
          disabled={
            isSubmitting
          }
          {...form.register(
            "new_password",
          )}
        />

        {form.formState.errors
          .new_password ? (
          <p className="text-sm text-destructive">
            {
              form.formState.errors
                .new_password
                .message
            }
          </p>
        ) : null}
      </div>

      <div className="space-y-2">
        <Label htmlFor="reset-password-confirm">
          Confirm new password
        </Label>

        <Input
          id="reset-password-confirm"
          type="password"
          autoComplete="new-password"
          placeholder="Confirm your new password"
          disabled={
            isSubmitting
          }
          {...form.register(
            "confirm_password",
          )}
        />

        {form.formState.errors
          .confirm_password ? (
          <p className="text-sm text-destructive">
            {
              form.formState.errors
                .confirm_password
                .message
            }
          </p>
        ) : null}
      </div>

      <div className="pt-6">
        <Button
          type="submit"
          className="w-full"
          disabled={
            isSubmitting
          }
        >
          {isSubmitting
            ? "Resetting password..."
            : "Reset password"}
        </Button>

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
    </AppForm>
  );
}
