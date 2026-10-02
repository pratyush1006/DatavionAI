/**
 * Contact information section.
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
  OrganizationFormValues,
} from "../../../domain";

export type ContactInformationProps =
  Readonly<{
    form:
      UseFormReturn<OrganizationFormValues>;
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
          autoComplete="email"
        />

        <ControlledInput
          form={form}
          name="supportEmail"
          label="Support Email"
          type="email"
          placeholder="support@organization.com"
          required
          autoComplete="email"
        />

        <ControlledInput
          form={form}
          name="phone"
          label="Phone Number"
          placeholder="+91 9876543210"
          required
          autoComplete="tel"
        />

        <ControlledInput
          form={form}
          name="website"
          label="Website"
          placeholder="https://organization.com"
          type="url"
          autoComplete="url"
        />
      </FormGrid>
    </FormSection>
  );
}
