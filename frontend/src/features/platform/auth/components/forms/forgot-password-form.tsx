/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/auth/components/forms/forgot-password-form.tsx
 * =============================================================================
 *
 * Forgot-password request form.
 *
 * Responsibilities
 * ----------------
 * - Own React Hook Form state.
 * - Validate the email address.
 * - Delegate submission to the page layer.
 * - Render the password-reset request UI.
 * - Render contextual request feedback below the action.
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
  forgotPasswordDefaults,
} from "../../domain/defaults";

import {
  forgotPasswordSchema,
  type ForgotPasswordFormValues,
} from "../../domain/schema";

/* =============================================================================
 * Props
 * =============================================================================
 */

export type ForgotPasswordFormProps =
  Readonly<{
    isSubmitting?: boolean;

    successMessage?:
      string | null;

    errorMessage?:
      string | null;

    infoMessage?:
      string | null;

    onSubmit: (
      values: ForgotPasswordFormValues,
    ) => void | Promise<void>;
  }>;

/* =============================================================================
 * Component
 * =============================================================================
 */

export function ForgotPasswordForm({
  isSubmitting = false,
  successMessage,
  errorMessage,
  infoMessage,
  onSubmit,
}: ForgotPasswordFormProps) {
  const form =
    useForm<ForgotPasswordFormValues>({
      resolver:
        zodResolver(
          forgotPasswordSchema,
        ),

      defaultValues:
        forgotPasswordDefaults,

      mode: "onBlur",
    });

  return (
    <AppForm
      onSubmit={form.handleSubmit(
        onSubmit,
      )}
    >
      <div className="space-y-2">
        <Label htmlFor="forgot-password-email">
          Email address
        </Label>

        <Input
          id="forgot-password-email"
          type="email"
          autoComplete="email"
          placeholder="you@example.com"
          disabled={
            isSubmitting
          }
          {...form.register(
            "email",
          )}
        />

        {form.formState.errors.email ? (
          <p className="text-sm text-destructive">
            {
              form.formState.errors
                .email.message
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
            ? "Sending code..."
            : "Send verification code"}
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
