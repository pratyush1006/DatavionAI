/**
 * Enterprise form field wrapper.
 */

import type { ReactNode } from "react";

import {
  FormControl,
  FormDescription,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";

export type FormFieldGroupProps =
  Readonly<{
    label: string;

    children: ReactNode;

    required?: boolean;

    description?: string;

    className?: string;
  }>;

export function FormFieldGroup({
  label,
  children,
  required = false,
  description,
  className,
}: FormFieldGroupProps) {
  return (
    <FormItem className={className}>
      <FormLabel>
        {label}

        {required && (
          <span className="ml-1 text-destructive">
            *
          </span>
        )}
      </FormLabel>

      <FormControl>
        {children as React.ReactElement}
      </FormControl>

      {description && (
        <FormDescription>
          {description}
        </FormDescription>
      )}

      <FormMessage />
    </FormItem>
  );
}
