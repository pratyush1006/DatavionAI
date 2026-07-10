/**
 * Organization form.
 */

"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import {
  useEffect,
  useMemo,
} from "react";
import { useForm } from "react-hook-form";

import {
  AppForm,
  FormActions,
} from "@/components/common/forms";

import { Form } from "@/components/ui/form";

import {
  organizationDefaults,
  organizationSchema,
  type OrganizationFormValues,
} from "../../domain";

import {
  AddressInformation,
  ContactInformation,
  GeneralInformation,
} from "./sections";

export type OrganizationFormProps = Readonly<{
  defaultValues?: Partial<OrganizationFormValues>;

  isSubmitting?: boolean;

  isEdit?: boolean;

  onSubmit: (
    values: OrganizationFormValues,
  ) => void | Promise<void>;

  onCancel?: () => void;
}>;

export function OrganizationForm({
  defaultValues,
  isSubmitting = false,
  isEdit = false,
  onSubmit,
  onCancel,
}: OrganizationFormProps) {
  const initialValues = useMemo(
    () => ({
      ...organizationDefaults,
      ...defaultValues,
    }),
    [defaultValues],
  );

  const form =
    useForm<OrganizationFormValues>({
      resolver: zodResolver(
        organizationSchema,
      ),

      defaultValues: initialValues,

      mode: "onBlur",
    });

  useEffect(() => {
    form.reset(initialValues);
  }, [
    form,
    initialValues,
  ]);

  return (
    <Form {...form}>
      <AppForm
        onSubmit={form.handleSubmit(
          onSubmit,
        )}
      >
        <GeneralInformation
          form={form}
          isEdit={isEdit}
        />

        <ContactInformation
          form={form}
        />

        <AddressInformation
          form={form}
        />

        <FormActions
          isEdit={isEdit}
          isSubmitting={isSubmitting}
          onCancel={onCancel}
          submitLabel={
            isEdit
              ? "Update Organization"
              : "Create Organization"
          }
          submittingLabel={
            isEdit
              ? "Updating..."
              : "Creating..."
          }
        />
      </AppForm>
    </Form>
  );
}
