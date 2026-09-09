/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/employees/components/forms/sections/contact-information.tsx
 * =============================================================================
 *
 * Employee contact information.
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

export type ContactInformationProps =
  Readonly<{
    form:
      UseFormReturn<EmployeeFormValues>;
  }>;

export function ContactInformation({
  form,
}: ContactInformationProps) {
  return (
    <FormSection
      title="Contact Information"
      description="Work contact information for the employee."
    >
      <FormGrid>
        <ControlledInput
          form={form}
          name="workEmail"
          label="Work Email"
          placeholder="employee@hospital.com"
          type="email"
        />

        <ControlledInput
          form={form}
          name="phoneNumber"
          label="Phone Number"
          placeholder="+91 9876543210"
        />
      </FormGrid>
    </FormSection>
  );
}
