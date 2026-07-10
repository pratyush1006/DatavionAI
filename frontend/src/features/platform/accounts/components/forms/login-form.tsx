/**
 * Login form.
 */

"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";

import { AppForm } from "@/components/common/forms/app-form";

import { loginDefaults } from "../../domain/defaults";
import {
  loginSchema,
  type LoginFormValues,
} from "../../domain/schema";

import { LoginActions } from "./login-actions";
import { LoginFields } from "./login-fields";

export type LoginFormProps = Readonly<{
  isSubmitting?: boolean;
  onSubmit: (
    values: LoginFormValues,
  ) => void | Promise<void>;
}>;

export function LoginForm({
  isSubmitting = false,
  onSubmit,
}: LoginFormProps) {
  const form = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),

    defaultValues: loginDefaults,

    mode: "onBlur",
  });

  return (
    <AppForm
      onSubmit={form.handleSubmit(onSubmit)}
    >
      <LoginFields form={form} />

      <LoginActions
        isSubmitting={isSubmitting}
      />
    </AppForm>
  );
}
