"use client";

/**
 * Login form fields.
 */

import type { UseFormReturn } from "react-hook-form";

import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

import type { LoginFormValues } from "../../domain/schema";

type LoginFieldsProps = Readonly<{
  form: UseFormReturn<LoginFormValues>;
}>;

export function LoginFields({
  form,
}: LoginFieldsProps) {
  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <Label htmlFor="email">
          Email
        </Label>

        <Input
          id="email"
          type="email"
          autoComplete="email"
          placeholder="admin@datavion.ai"
          {...form.register("email")}
        />

        {form.formState.errors.email && (
          <p className="text-sm text-destructive">
            {form.formState.errors.email.message}
          </p>
        )}
      </div>

      <div className="space-y-2">
        <Label htmlFor="password">
          Password
        </Label>

        <Input
          id="password"
          type="password"
          autoComplete="current-password"
          {...form.register("password")}
        />

        {form.formState.errors.password && (
          <p className="text-sm text-destructive">
            {form.formState.errors.password.message}
          </p>
        )}
      </div>
    </div>
  );
}
