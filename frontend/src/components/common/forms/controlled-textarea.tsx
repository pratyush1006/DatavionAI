/**
 * Controlled textarea integrated with react-hook-form.
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
  Textarea,
} from "@/components/ui/textarea";

import {
  FormFieldGroup,
} from "./form-field-group";

export type ControlledTextareaProps<
  TFieldValues extends FieldValues,
> = Readonly<{
  form: UseFormReturn<TFieldValues>;

  name: FieldPath<TFieldValues>;

  label: string;

  placeholder?: string;

  description?: string;

  rows?: number;

  required?: boolean;

  disabled?: boolean;

  className?: string;
}>;

export function ControlledTextarea<
  TFieldValues extends FieldValues,
>({
  form,
  name,
  label,
  placeholder,
  description,
  rows = 4,
  required = false,
  disabled = false,
  className,
}: ControlledTextareaProps<TFieldValues>) {
  return (
    <FormField
      control={form.control}
      name={name}
      render={({ field }) => (
        <FormFieldGroup
          label={label}
          description={description}
          required={required}
          className={className}
        >
          <Textarea
            {...field}
            rows={rows}
            disabled={disabled}
            placeholder={placeholder}
            value={field.value ?? ""}
          />
        </FormFieldGroup>
      )}
    />
  );
}
