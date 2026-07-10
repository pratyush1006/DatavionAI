/**
 * General organization information section.
 */

"use client";

import type { UseFormReturn } from "react-hook-form";

import {
  ControlledInput,
  ControlledSelect,
  ControlledSwitch,
  FormGrid,
  FormSection,
} from "@/components/common/forms";

import {
  organizationTypeOptions,
  type OrganizationFormValues,
} from "../../../domain";

export type GeneralInformationProps = Readonly<{
  form: UseFormReturn<OrganizationFormValues>;

  isEdit?: boolean;
}>;

export function GeneralInformation({
  form,
  isEdit = false,
}: GeneralInformationProps) {
  return (
    <FormSection
      title="General Information"
      description="Basic details used to identify the organization."
    >
      <FormGrid>
        <ControlledInput
          form={form}
          name="name"
          label="Organization Name"
          placeholder="Ayush Hospital"
          required
        />

        <ControlledInput
          form={form}
          name="code"
          label="Organization Code"
          placeholder="AY101"
          description="Uppercase letters and numbers only."
          required
          disabled={isEdit}
          transform={(value) =>
            value.toUpperCase()
          }
        />

        <ControlledSelect
          form={form}
          name="organizationType"
          label="Organization Type"
          placeholder="Select organization type"
          options={organizationTypeOptions}
          required
        />

        <ControlledSwitch
          form={form}
          name="isActive"
          label="Active"
          description="Enable or disable this organization."
        />
      </FormGrid>
    </FormSection>
  );
}
