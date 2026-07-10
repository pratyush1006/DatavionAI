/**
 * Contact information section.
 */

"use client";

import type { UseFormReturn } from "react-hook-form";

import {
  ControlledInput,
  FormGrid,
  FormSection,
} from "@/components/common/forms";

import type {
  OrganizationFormValues,
} from "../../../domain";

export type ContactInformationProps = Readonly<{
  form: UseFormReturn<OrganizationFormValues>;
}>;

export function ContactInformation({
  form,
}: ContactInformationProps) {
  return (
    <FormSection
      title="Contact Information"
      description="Primary communication details for the organization."
    >
      <FormGrid>
        <ControlledInput
          form={form}
          name="email"
          label="Email Address"
          type="email"
          placeholder="info@organization.com"
          required
        />

        <ControlledInput
          form={form}
          name="phone"
          label="Phone Number"
          placeholder="+91 9876543210"
          required
        />
      </FormGrid>
    </FormSection>
  );
}
