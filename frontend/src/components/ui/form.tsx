"use client";

import * as React from "react";
import {
  Controller,
  FormProvider,
  useFormContext,
  useFormState,
  type ControllerProps,
  type FieldPath,
  type FieldValues,
} from "react-hook-form";

import { cn } from "@/lib/utils";

const Form = FormProvider;

type FormFieldContextValue<
  TFieldValues extends FieldValues = FieldValues,
  TName extends FieldPath<TFieldValues> = FieldPath<TFieldValues>,
> = {
  name: TName;
};

const FormFieldContext =
  React.createContext<FormFieldContextValue>(
    {} as FormFieldContextValue,
  );

function FormField<
  TFieldValues extends FieldValues = FieldValues,
  TName extends FieldPath<TFieldValues> = FieldPath<TFieldValues>,
>({
  ...props
}: ControllerProps<TFieldValues, TName>) {
  return (
    <FormFieldContext.Provider
      value={{ name: props.name }}
    >
      <Controller {...props} />
    </FormFieldContext.Provider>
  );
}

const FormItemContext = React.createContext<{
  id: string;
}>({} as { id: string });

function FormItem({
  className,
  ...props
}: React.ComponentProps<"div">) {
  const id = React.useId();

  return (
    <FormItemContext.Provider value={{ id }}>
      <div
        className={cn(
          "space-y-2",
          className,
        )}
        {...props}
      />
    </FormItemContext.Provider>
  );
}

function useFormField() {
  const fieldContext =
    React.useContext(FormFieldContext);

  const itemContext =
    React.useContext(FormItemContext);

  const {
    getFieldState,
  } = useFormContext();

  const formState =
    useFormState({
      name: fieldContext.name,
    });

  const fieldState = getFieldState(
    fieldContext.name,
    formState,
  );

  const { id } = itemContext;

  return {
    id,
    name: fieldContext.name,
    formItemId: `${id}-form-item`,
    formDescriptionId: `${id}-form-item-description`,
    formMessageId: `${id}-form-item-message`,
    ...fieldState,
  };
}

function FormLabel({
  className,
  ...props
}: React.ComponentProps<"label">) {
  const {
    error,
    formItemId,
  } = useFormField();

  return (
    <label
      htmlFor={formItemId}
      className={cn(
        "text-sm font-medium",
        error &&
          "text-destructive",
        className,
      )}
      {...props}
    />
  );
}

function FormControl({
  ...props
}: React.ComponentProps<"div">) {
  const {
    error,
    formItemId,
    formDescriptionId,
    formMessageId,
  } = useFormField();

  return (
    <div
      id={formItemId}
      aria-describedby={
        error
          ? `${formDescriptionId} ${formMessageId}`
          : formDescriptionId
      }
      aria-invalid={!!error}
      {...props}
    />
  );
}

function FormDescription({
  className,
  ...props
}: React.ComponentProps<"p">) {
  const {
    formDescriptionId,
  } = useFormField();

  return (
    <p
      id={formDescriptionId}
      className={cn(
        "text-sm text-muted-foreground",
        className,
      )}
      {...props}
    />
  );
}

function FormMessage({
  className,
  children,
  ...props
}: React.ComponentProps<"p">) {
  const {
    error,
    formMessageId,
  } = useFormField();

  const body =
    error?.message?.toString() ??
    children;

  if (!body) {
    return null;
  }

  return (
    <p
      id={formMessageId}
      className={cn(
        "text-sm font-medium text-destructive",
        className,
      )}
      {...props}
    >
      {body}
    </p>
  );
}

export {
  Form,
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormDescription,
  FormMessage,
  useFormField,
};
