/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/employees/components/forms/employee-form.tsx
 * =============================================================================
 *
 * Employee create/update form.
 *
 * Responsibilities
 * ----------------
 * - Own React Hook Form state.
 * - Validate employee input with the domain Zod schema.
 * - Surface validation failures consistently.
 * - Delegate successful submission to the parent dialog/page.
 * - Keep mutation/business logic outside the form.
 *
 * Architecture
 * ------------
 *
 * EmployeeForm
 *      |
 *      +--> React Hook Form
 *      |
 *      +--> Zod employeeSchema
 *      |
 *      +--> EmployeeInformation
 *      +--> ContactInformation
 *      +--> EmploymentInformation
 *      |
 *      +--> parent onSubmit()
 *
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

import {
  useForm,
} from "react-hook-form";

import {
  toast,
} from "sonner";

import {
  AppForm,
  FormActions,
} from "@/components/common/forms";

import {
  Form,
} from "@/components/ui/form";

import {
  employeeDefaults,
  employeeSchema,
  type EmployeeFormValues,
} from "../../domain";

import {
  ContactInformation,
  EmployeeInformation,
  EmploymentInformation,
} from "./sections";

/* =============================================================================
 * Props
 * =============================================================================
 */

export type EmployeeFormProps =
  Readonly<{
    /**
     * Initial form values.
     *
     * Used primarily by the edit form.
     */
    defaultValues?: Partial<EmployeeFormValues>;

    /**
     * Whether the parent mutation is currently submitting.
     */
    isSubmitting?: boolean;

    /**
     * Whether the form is being used for editing.
     */
    isEdit?: boolean;

    /**
     * Called only after successful client-side validation.
     */
    onSubmit: (
      values: EmployeeFormValues,
    ) => void | Promise<void>;

    /**
     * Optional cancellation handler.
     */
    onCancel?: () => void;
  }>;

/* =============================================================================
 * Component
 * =============================================================================
 */

export function EmployeeForm({
  defaultValues,
  isSubmitting = false,
  isEdit = false,
  onSubmit,
  onCancel,
}: EmployeeFormProps) {
  /**
   * Merge domain defaults with supplied values.
   *
   * Memoization keeps the object stable unless the caller actually changes
   * defaultValues.
   */
  const initialValues =
    useMemo(
      () => ({
        ...employeeDefaults,
        ...defaultValues,
      }),
      [defaultValues],
    );

  /**
   * React Hook Form owns client-side form state.
   *
   * Zod remains the authoritative frontend validation schema.
   */
  const form =
    useForm<EmployeeFormValues>({
      resolver:
        zodResolver(
          employeeSchema,
        ),

      defaultValues:
        initialValues,

      mode: "onBlur",

      /**
       * Focus the first invalid field when submission fails validation.
       */
      shouldFocusError: true,
    });

  /**
   * Reset the form when the supplied defaults change.
   *
   * This is important for edit dialogs where the selected employee can
   * change without remounting the form component.
   */
  useEffect(() => {
    form.reset(
      initialValues,
    );
  }, [
    form,
    initialValues,
  ]);

  /**
   * Handle invalid submission explicitly.
   *
   * Previously the form called handleSubmit(onSubmit) without an invalid
   * callback. Therefore, when required fields such as organization or
   * joiningDate were empty, the click appeared to do nothing.
   *
   * React Hook Form still rejected the submission correctly, but the user
   * received no clear form-level feedback.
   */
  function handleInvalidSubmit(): void {
    toast.error(
      "Please fix the highlighted employee fields before submitting.",
    );
  }

  /**
   * Render.
   */
  return (
    <Form {...form}>
      <AppForm
        onSubmit={
          form.handleSubmit(
            onSubmit,
            handleInvalidSubmit,
          )
        }
      >
        <EmployeeInformation
          form={form}
          isEdit={isEdit}
        />

        <ContactInformation
          form={form}
        />

        <EmploymentInformation
          form={form}
          isEdit={isEdit}
        />

        <FormActions
          isEdit={isEdit}
          isSubmitting={
            isSubmitting
          }
          onCancel={onCancel}
          submitLabel={
            isEdit
              ? "Update Employee"
              : "Create Employee"
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
