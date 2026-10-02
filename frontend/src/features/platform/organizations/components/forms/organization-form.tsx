/**
 * =============================================================================
 * DatavionOS
 * File:
 * src/features/platform/organizations/components/forms/organization-form.tsx
 * =============================================================================
 *
 * Organization create/edit form.
 *
 * Responsibilities
 * ----------------
 * - Validate organization form data.
 * - Render organization form sections.
 * - Handle client-side validation feedback.
 * - Render contextual mutation feedback below the action buttons.
 * - Keep mutation feedback separate from global toast notifications.
 * =============================================================================
 */

"use client";

import {
  zodResolver,
} from "@hookform/resolvers/zod";

import {
  useEffect,
  useMemo,
} from "react";

import { useQuery } from "@tanstack/react-query";

import {
  useForm,
} from "react-hook-form";

import {
  AppForm,
  FormActions,
} from "@/components/common/forms";

import {
  Form,
} from "@/components/ui/form";

import {
  organizationDefaults,
  organizationSchema,
  type OrganizationFormValues,
} from "../../domain";

import { organizationQueries } from "../../api";

import {
  AddressInformation,
  ContactInformation,
  GeneralInformation,
  LegalInformation,
} from "./sections";

/* =============================================================================
 * Props
 * =============================================================================
 */

export type OrganizationFormProps =
  Readonly<{
    defaultValues?: Partial<OrganizationFormValues>;

    isSubmitting?: boolean;

    isEdit?: boolean;

    /**
     * Contextual success message rendered directly below the submit button.
     */
    successMessage?: string | null;

    /**
     * Contextual error message rendered directly below the submit button.
     */
    errorMessage?: string | null;

    /**
     * Contextual informational message rendered directly below the submit button.
     */
    infoMessage?: string | null;

    onSubmit: (
      values: OrganizationFormValues,
    ) => void | Promise<void>;

    onCancel?: () => void;
  }>;

/* =============================================================================
 * Component
 * =============================================================================
 */

export function OrganizationForm({
  defaultValues,
  isSubmitting = false,
  isEdit = false,
  successMessage,
  errorMessage,
  infoMessage,
  onSubmit,
  onCancel,
}: OrganizationFormProps) {
  const initialValues =
    useMemo(
      () => ({
        ...organizationDefaults,
        ...defaultValues,
      }),
      [defaultValues],
    );

  const form =
    useForm<OrganizationFormValues>({
      resolver:
        zodResolver(
          organizationSchema,
        ),
      defaultValues:
        initialValues,
      mode: "onBlur",
    });

  const categoriesQuery = useQuery(organizationQueries.categories());
  const typesQuery = useQuery(organizationQueries.types());
  const sizesQuery = useQuery(organizationQueries.sizes());

  const firstError =
    Object.values(
      form.formState.errors,
    ).find(
      (error) =>
        typeof error?.message ===
        "string",
    );

  useEffect(() => {
    form.reset(
      initialValues,
    );
  }, [
    form,
    initialValues,
  ]);

  return (
    <Form {...form}>
      <AppForm
        onSubmit={form.handleSubmit(
          onSubmit,
          () =>
            form.setFocus(
              "name",
            ),
        )}
      >
        <GeneralInformation
          form={form}
          isEdit={isEdit}
          categoryOptions={categoriesQuery.data}
          organizationTypeOptions={typesQuery.data}
          sizeOptions={sizesQuery.data}
        />

        <ContactInformation
          form={form}
        />

        <AddressInformation
          form={form}
        />

        <LegalInformation
          form={form}
        />

        <FormActions
          isEdit={isEdit}
          isSubmitting={
            isSubmitting
          }
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
          successMessage={
            successMessage
          }
          errorMessage={
            errorMessage
          }
          infoMessage={
            infoMessage
          }
        >
          {firstError?.message && (
            <p
              role="alert"
              className="mr-auto text-sm text-destructive"
            >
              {
                firstError.message
              }
            </p>
          )}
        </FormActions>
      </AppForm>
    </Form>
  );
}
