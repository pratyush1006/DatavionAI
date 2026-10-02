/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/auth/components/forms/login-form.tsx
 * =============================================================================
 *
 * Login form.
 *
 * Responsibilities
 * ----------------
 * - Own React Hook Form state.
 * - Apply login validation.
 * - Connect form submission to the authentication feature.
 * - Render login fields and actions.
 * - Pass contextual mutation feedback to the action component.
 *
 * Design Principles
 * -----------------
 * - Strong TypeScript typing.
 * - Schema driven validation.
 * - No API calls.
 * - No authentication business logic.
 * - Reusable.
 * - Enterprise Ready.
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
  AppForm,
} from "@/components/common/forms/app-form";

import {
  loginDefaults,
} from "../../domain/defaults";

import {
  loginSchema,
  type LoginFormValues,
} from "../../domain/schema";

import {
  LoginActions,
} from "./login-actions";

import {
  LoginFields,
} from "./login-fields";

/* =============================================================================
 * Props
 * =============================================================================
 */

export type LoginFormProps =
  Readonly<{
    isSubmitting?: boolean;

    successMessage?:
      string | null;

    errorMessage?:
      string | null;

    infoMessage?:
      string | null;

    onSubmit: (
      values: LoginFormValues,
    ) => void | Promise<void>;
  }>;

/* =============================================================================
 * Component
 * =============================================================================
 */

export function LoginForm({
  isSubmitting = false,
  successMessage,
  errorMessage,
  infoMessage,
  onSubmit,
}: LoginFormProps) {
  const form =
    useForm<LoginFormValues>({
      resolver:
        zodResolver(
          loginSchema,
        ),

      defaultValues:
        loginDefaults,

      mode: "onBlur",
    });

  return (
    <AppForm
      onSubmit={
        form.handleSubmit(
          onSubmit,
        )
      }
    >
      <LoginFields
        form={form}
      />

      <LoginActions
        isSubmitting={
          isSubmitting
        }
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
    </AppForm>
  );
}
