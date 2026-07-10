"use client";

/**
 * Reusable form components built on react-hook-form.
 */

import * as React from "react";

import {
  Controller,
  FormProvider,
  useController,
  useFormContext,
  type ControllerProps,
  type FieldPath,
  type FieldValues,
} from "react-hook-form";

import { Label } from "@/components/ui/label";

import { cn } from "@/lib/utils";

export const Form = FormProvider;

const FormFieldContext =
  React.createContext<{
    name: string;
  } | null>(null);

export function FormField<
  TFieldValues extends FieldValues,
  TName extends FieldPath<TFieldValues>,
>(
  props: ControllerProps<TFieldValues, TName>,
) {
  return (
    <FormFieldContext.Provider
      value={{ name: props.name }}
    >
      <Controller {...props} />
    </FormFieldContext.Provider>
  );
}

export function FormItem({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn("space-y-2", className)}
      {...props}
    />
  );
}

export function FormLabel(
  props: React.ComponentProps<typeof Label>,
) {
  return <Label {...props} />;
}

export function FormControl({
  children,
}: {
  children: React.ReactElement;
}) {
  const field = useFormField();

  return React.cloneElement(children, {
    "aria-invalid": !!field.error,
  });
}

export function FormDescription({
  className,
  ...props
}: React.HTMLAttributes<HTMLParagraphElement>) {
  return (
    <p
      className={cn(
        "text-sm text-muted-foreground",
        className,
      )}
      {...props}
    />
  );
}

export function FormMessage({
  className,
  ...props
}: React.HTMLAttributes<HTMLParagraphElement>) {
  const { error } = useFormField();

  if (!error) {
    return null;
  }

  return (
    <p
      className={cn(
        "text-sm text-destructive",
        className,
      )}
      {...props}
    >
      {String(error.message)}
    </p>
  );
}

function useFormField() {
  const fieldContext =
    React.useContext(FormFieldContext);

  if (!fieldContext) {
    throw new Error(
      "useFormField must be used inside FormField.",
    );
  }

  const { getFieldState } = useFormContext();

  const state = getFieldState(
    fieldContext.name,
  );

  return {
    name: fieldContext.name,
    error: state.error,
  };
}
