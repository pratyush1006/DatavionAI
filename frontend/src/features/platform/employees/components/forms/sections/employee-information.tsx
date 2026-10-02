/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/employees/components/forms/sections/employee-information.tsx
 * =============================================================================
 *
 * Employee identity and organization information.
 * =============================================================================
 */

"use client";

import type {
  UseFormReturn,
} from "react-hook-form";

import {
  ControlledInput,
  FormGrid,
  FormSection,
} from "@/components/common/forms";

import type {
  EmployeeFormValues,
} from "../../../domain";

export type EmployeeInformationProps =
  Readonly<{
    form:
      UseFormReturn<EmployeeFormValues>;
    isEdit?: boolean;
  }>;

export function EmployeeInformation({
  form,
  isEdit = false,
}: EmployeeInformationProps) {
  return (
    <FormSection
      title="Employee Information"
      description="Core identity and organization information."
    >
      <FormGrid>
        <ControlledInput
          form={form}
          name="organization"
          label="Organization"
          placeholder="Organization ID"
          required
          disabled={isEdit}
        />

        <ControlledInput
          form={form}
          name="user"
          label="User"
          placeholder="User ID"
          description="Optional linked platform user."
          disabled={isEdit}
        />

        <ControlledInput
          form={form}
          name="employeeCode"
          label="Employee Code"
          placeholder="EMP001"
          description="Unique employee code within the organization."
          required
          disabled={isEdit}
          transform={(value) =>
            value.toUpperCase()
          }
        />

        <ControlledInput
          form={form}
          name="designation"
          label="Designation"
          placeholder="Senior Physician"
          required
        />
      </FormGrid>
    </FormSection>
  );
}
