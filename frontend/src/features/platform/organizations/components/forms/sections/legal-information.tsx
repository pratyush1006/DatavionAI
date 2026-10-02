/**
 * Legal information section.
 */

"use client";

import type {
  UseFormReturn,
} from "react-hook-form";

import {
  ControlledInput,
  ControlledTextarea,
  FormGrid,
  FormSection,
} from "@/components/common/forms";

import type {
  OrganizationFormValues,
} from "../../../domain";

export type LegalInformationProps =
  Readonly<{
    form:
      UseFormReturn<OrganizationFormValues>;
  }>;

export function LegalInformation({
  form,
}: LegalInformationProps) {
  return (
    <FormSection
      title="Legal & Compliance"
      description="Registration, tax, licensing and accreditation information."
    >
      <FormGrid>
        <ControlledInput
          form={form}
          name="registrationNumber"
          label="Registration Number"
          placeholder="REG-123456"
          required
        />

        <ControlledInput
          form={form}
          name="taxNumber"
          label="Tax / GST Number"
          placeholder="GSTIN123456789"
          required
        />

        <ControlledInput
          form={form}
          name="licenseNumber"
          label="Healthcare License Number"
          placeholder="LIC-123456"
          required
        />

        <ControlledInput
          form={form}
          name="accreditation"
          label="Accreditation"
          placeholder="NABH / NABL"
          required
        />

        <ControlledTextarea
          form={form}
          name="description"
          label="Description"
          placeholder="Describe the organization and its services."
          rows={4}
          required
          className="lg:col-span-2"
        />
      </FormGrid>
    </FormSection>
  );
}
