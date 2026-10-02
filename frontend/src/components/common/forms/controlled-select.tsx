/**
 * Controlled select integrated with react-hook-form.
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
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

import { FormFieldGroup } from "./form-field-group";

export type SelectOption = Readonly<{
  value: string;
  label: string;
}>;

export type ControlledSelectProps<
  TFieldValues extends FieldValues,
> = Readonly<{
  form: UseFormReturn<TFieldValues>;

  name: FieldPath<TFieldValues>;

  label: string;

  placeholder?: string;

  description?: string;

  options: readonly SelectOption[];

  required?: boolean;

  disabled?: boolean;

  className?: string;
}>;

export function ControlledSelect<
  TFieldValues extends FieldValues,
>({
  form,
  name,
  label,
  placeholder = "Select an option",
  description,
  options,
  required = false,
  disabled = false,
  className,
}: ControlledSelectProps<TFieldValues>) {
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
          <Select
            value={field.value}
            onValueChange={field.onChange}
            disabled={disabled}
          >
            <SelectTrigger>
              <SelectValue
                placeholder={placeholder}
              />
            </SelectTrigger>

            <SelectContent>
              {options.map((option) => (
                <SelectItem
                  key={option.value}
                  value={option.value}
                >
                  {option.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </FormFieldGroup>
      )}
    />
  );
}
