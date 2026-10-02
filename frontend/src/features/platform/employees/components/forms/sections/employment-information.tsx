/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/employees/components/forms/sections/employment-information.tsx
 * =============================================================================
 *
 * Employee employment information.
 * =============================================================================
 */

"use client";

import type {
  UseFormReturn,
} from "react-hook-form";

import {
  ControlledInput,
  ControlledSelect,
  FormGrid,
  FormSection,
} from "@/components/common/forms";

import {
  employmentTypeOptions,
  type EmployeeFormValues,
} from "../../../domain";

export type EmploymentInformationProps =
  Readonly<{
    form:
      UseFormReturn<EmployeeFormValues>;
    isEdit?: boolean;
  }>;

export function EmploymentInformation({
  form,
  isEdit = false,
}: EmploymentInformationProps) {
  return (
    <FormSection
      title="Employment Information"
      description="Employment type and lifecycle information."
    >
      <FormGrid>
        <ControlledSelect
          form={form}
          name="employmentType"
          label="Employment Type"
          placeholder="Select employment type"
          options={
            employmentTypeOptions
          }
          required
        />

        <ControlledInput
          form={form}
          name="joiningDate"
          label="Joining Date"
          type="date"
          required
          disabled={isEdit}
        />
      </FormGrid>
    </FormSection>
  );
}
