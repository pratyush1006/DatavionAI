/**
 * Controlled input integrated with react-hook-form.
 */

"use client";

import type {
  FieldPath,
  FieldValues,
  UseFormReturn,
} from "react-hook-form";

import { FormField } from "@/components/ui/form";
import { Input } from "@/components/ui/input";

import { FormFieldGroup } from "./form-field-group";

export type ControlledInputProps<
  TFieldValues extends FieldValues,
> = Readonly<{
  form: UseFormReturn<TFieldValues>;

  name: FieldPath<TFieldValues>;

  label: string;

  placeholder?: string;

  description?: string;

  type?: React.HTMLInputTypeAttribute;

  disabled?: boolean;

  required?: boolean;

  autoComplete?: string;

  className?: string;

  transform?: (
    value: string,
  ) => string;
}>;

export function ControlledInput<
  TFieldValues extends FieldValues,
>({
  form,
  name,
  label,
  placeholder,
  description,
  type = "text",
  disabled = false,
  required = false,
  autoComplete,
  className,
  transform,
}: ControlledInputProps<TFieldValues>) {
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
          <Input
            {...field}
            type={type}
            disabled={disabled}
            placeholder={placeholder}
            autoComplete={autoComplete}
            value={field.value ?? ""}
            onChange={(event) =>
              field.onChange(
                transform
                  ? transform(
                      event.target.value,
                    )
                  : event.target.value,
              )
            }
          />
        </FormFieldGroup>
      )}
    />
  );
}
