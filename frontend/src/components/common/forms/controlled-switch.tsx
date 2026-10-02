/**
 * Controlled switch integrated with react-hook-form.
 */

"use client";

import type {
  FieldPath,
  FieldValues,
  UseFormReturn,
} from "react-hook-form";

import {
  FormField,
} from "@/components/ui/form";

import {
  Switch,
} from "@/components/ui/switch";

import { cn } from "@/lib/utils";

export type ControlledSwitchProps<
  TFieldValues extends FieldValues,
> = Readonly<{
  form: UseFormReturn<TFieldValues>;

  name: FieldPath<TFieldValues>;

  label: string;

  description?: string;

  disabled?: boolean;

  className?: string;
}>;

export function ControlledSwitch<
  TFieldValues extends FieldValues,
>({
  form,
  name,
  label,
  description,
  disabled = false,
  className,
}: ControlledSwitchProps<TFieldValues>) {
  return (
    <FormField
      control={form.control}
      name={name}
      render={({ field }) => (
        <div
          className={cn(
            "flex items-start justify-between rounded-xl border border-border bg-card p-5",
            className,
          )}
        >
          <div className="space-y-1">
            <h4 className="text-sm font-medium">
              {label}
            </h4>

            {description && (
              <p className="text-sm text-muted-foreground">
                {description}
              </p>
            )}
          </div>

          <Switch
            checked={Boolean(field.value)}
            onCheckedChange={field.onChange}
            disabled={disabled}
          />
        </div>
      )}
    />
  );
}
