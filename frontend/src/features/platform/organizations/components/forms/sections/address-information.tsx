/**
 * Address information section.
 */

"use client";

import type { UseFormReturn } from "react-hook-form";

import {
  ControlledInput,
  ControlledTextarea,
  FormGrid,
  FormSection,
} from "@/components/common/forms";

import type {
  OrganizationFormValues,
} from "../../../domain";

export type AddressInformationProps = Readonly<{
  form: UseFormReturn<OrganizationFormValues>;
}>;

export function AddressInformation({
  form,
}: AddressInformationProps) {
  return (
    <FormSection
      title="Address"
      description="Location information for the organization."
    >
      <FormGrid>
        <ControlledInput
          form={form}
          name="country"
          label="Country"
          placeholder="India"
          required
          autoComplete="country-name"
        />

        <ControlledInput
          form={form}
          name="state"
          label="State"
          placeholder="Karnataka"
          required
          autoComplete="address-level1"
        />

        <ControlledInput
          form={form}
          name="city"
          label="City"
          placeholder="Bengaluru"
          required
          autoComplete="address-level2"
        />

        <ControlledTextarea
          form={form}
          name="address"
          label="Address"
          placeholder="Enter the complete organization address"
          rows={4}
          required
          className="lg:col-span-2"
        />
      </FormGrid>
    </FormSection>
  );
}
