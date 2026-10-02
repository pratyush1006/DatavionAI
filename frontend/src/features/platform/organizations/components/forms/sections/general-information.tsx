/**
 * =============================================================================
 * DatavionOS
 * File:
 * src/features/platform/organizations/components/forms/sections/general-information.tsx
 * =============================================================================
 */

"use client";

import type {
  UseFormReturn,
} from "react-hook-form";

import {
  ControlledInput,
  ControlledSelect,
  ControlledSwitch,
  FormGrid,
  FormSection,
  type SelectOption,
} from "@/components/common/forms";

import {
  organizationCategoryOptions,
  organizationSizeOptions,
  organizationStatusOptions,
  organizationTypeOptions,
  type OrganizationFormValues,
} from "../../../domain";

/* =============================================================================
 * Timezone options
 * =============================================================================
 *
 * DatavionOS stores timezone values as canonical IANA timezone identifiers.
 *
 * The list intentionally contains the globally relevant IANA zones used by
 * organizations. "Asia/Kolkata" is explicitly included because it is the
 * canonical timezone expected for India and is already used by DatavionOS.
 */

const timezoneOptions: SelectOption[] = [
  {
    value: "Africa/Cairo",
    label: "Africa/Cairo",
  },
  {
    value: "Africa/Johannesburg",
    label: "Africa/Johannesburg",
  },
  {
    value: "Africa/Lagos",
    label: "Africa/Lagos",
  },
  {
    value: "Africa/Nairobi",
    label: "Africa/Nairobi",
  },
  {
    value: "America/Argentina/Buenos_Aires",
    label: "America/Argentina/Buenos_Aires",
  },
  {
    value: "America/Chicago",
    label: "America/Chicago",
  },
  {
    value: "America/Denver",
    label: "America/Denver",
  },
  {
    value: "America/Los_Angeles",
    label: "America/Los_Angeles",
  },
  {
    value: "America/Mexico_City",
    label: "America/Mexico_City",
  },
  {
    value: "America/New_York",
    label: "America/New_York",
  },
  {
    value: "America/Phoenix",
    label: "America/Phoenix",
  },
  {
    value: "America/Sao_Paulo",
    label: "America/Sao_Paulo",
  },
  {
    value: "America/Toronto",
    label: "America/Toronto",
  },
  {
    value: "America/Vancouver",
    label: "America/Vancouver",
  },
  {
    value: "Asia/Bangkok",
    label: "Asia/Bangkok",
  },
  {
    value: "Asia/Dhaka",
    label: "Asia/Dhaka",
  },
  {
    value: "Asia/Dubai",
    label: "Asia/Dubai",
  },
  {
    value: "Asia/Hong_Kong",
    label: "Asia/Hong_Kong",
  },
  {
    value: "Asia/Jakarta",
    label: "Asia/Jakarta",
  },
  {
    value: "Asia/Jerusalem",
    label: "Asia/Jerusalem",
  },
  {
    value: "Asia/Karachi",
    label: "Asia/Karachi",
  },
  {
    value: "Asia/Kathmandu",
    label: "Asia/Kathmandu",
  },
  {
    value: "Asia/Kolkata",
    label: "Asia/Kolkata",
  },
  {
    value: "Asia/Kuala_Lumpur",
    label: "Asia/Kuala_Lumpur",
  },
  {
    value: "Asia/Manila",
    label: "Asia/Manila",
  },
  {
    value: "Asia/Riyadh",
    label: "Asia/Riyadh",
  },
  {
    value: "Asia/Seoul",
    label: "Asia/Seoul",
  },
  {
    value: "Asia/Shanghai",
    label: "Asia/Shanghai",
  },
  {
    value: "Asia/Singapore",
    label: "Asia/Singapore",
  },
  {
    value: "Asia/Taipei",
    label: "Asia/Taipei",
  },
  {
    value: "Asia/Tokyo",
    label: "Asia/Tokyo",
  },
  {
    value: "Asia/Yangon",
    label: "Asia/Yangon",
  },
  {
    value: "Atlantic/Reykjavik",
    label: "Atlantic/Reykjavik",
  },
  {
    value: "Australia/Adelaide",
    label: "Australia/Adelaide",
  },
  {
    value: "Australia/Brisbane",
    label: "Australia/Brisbane",
  },
  {
    value: "Australia/Melbourne",
    label: "Australia/Melbourne",
  },
  {
    value: "Australia/Perth",
    label: "Australia/Perth",
  },
  {
    value: "Australia/Sydney",
    label: "Australia/Sydney",
  },
  {
    value: "Europe/Amsterdam",
    label: "Europe/Amsterdam",
  },
  {
    value: "Europe/Athens",
    label: "Europe/Athens",
  },
  {
    value: "Europe/Berlin",
    label: "Europe/Berlin",
  },
  {
    value: "Europe/Brussels",
    label: "Europe/Brussels",
  },
  {
    value: "Europe/Dublin",
    label: "Europe/Dublin",
  },
  {
    value: "Europe/Helsinki",
    label: "Europe/Helsinki",
  },
  {
    value: "Europe/Istanbul",
    label: "Europe/Istanbul",
  },
  {
    value: "Europe/Lisbon",
    label: "Europe/Lisbon",
  },
  {
    value: "Europe/London",
    label: "Europe/London",
  },
  {
    value: "Europe/Madrid",
    label: "Europe/Madrid",
  },
  {
    value: "Europe/Moscow",
    label: "Europe/Moscow",
  },
  {
    value: "Europe/Oslo",
    label: "Europe/Oslo",
  },
  {
    value: "Europe/Paris",
    label: "Europe/Paris",
  },
  {
    value: "Europe/Prague",
    label: "Europe/Prague",
  },
  {
    value: "Europe/Rome",
    label: "Europe/Rome",
  },
  {
    value: "Europe/Stockholm",
    label: "Europe/Stockholm",
  },
  {
    value: "Europe/Vienna",
    label: "Europe/Vienna",
  },
  {
    value: "Europe/Warsaw",
    label: "Europe/Warsaw",
  },
  {
    value: "Indian/Maldives",
    label: "Indian/Maldives",
  },
  {
    value: "Pacific/Auckland",
    label: "Pacific/Auckland",
  },
  {
    value: "Pacific/Fiji",
    label: "Pacific/Fiji",
  },
  {
    value: "Pacific/Guam",
    label: "Pacific/Guam",
  },
  {
    value: "Pacific/Honolulu",
    label: "Pacific/Honolulu",
  },
];

/* =============================================================================
 * Props
 * =============================================================================
 */

export type GeneralInformationProps =
  Readonly<{
    form:
      UseFormReturn<OrganizationFormValues>;

    isEdit?: boolean;

    /** Backend catalog values. Static choices are retained only as an outage fallback. */
    categoryOptions?: SelectOption[];
    organizationTypeOptions?: SelectOption[];
    sizeOptions?: SelectOption[];
  }>;

/* =============================================================================
 * Component
 * =============================================================================
 */

export function GeneralInformation({
  form,
  isEdit = false,
  categoryOptions,
  organizationTypeOptions: backendOrganizationTypeOptions,
  sizeOptions,
}: GeneralInformationProps) {
  const resolvedCategoryOptions = categoryOptions?.length
    ? categoryOptions
    : organizationCategoryOptions;
  const resolvedOrganizationTypeOptions = backendOrganizationTypeOptions?.length
    ? backendOrganizationTypeOptions
    : organizationTypeOptions;
  const resolvedSizeOptions = sizeOptions?.length
    ? sizeOptions
    : organizationSizeOptions;

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
          name="displayName"
          label="Display Name"
          placeholder="Ayush Hospital"
          required
        />

        <ControlledInput
          form={form}
          name="code"
          label="Organization Code"
          placeholder="AY101"
          description="Uppercase letters, numbers, '-' and '_' are allowed."
          required
          disabled={isEdit}
          transform={(value) =>
            value.toUpperCase()
          }
        />

        <ControlledInput
          form={form}
          name="slug"
          label="Slug"
          placeholder="ayush-hospital"
          description="Lowercase letters, numbers and hyphens only."
          required
          disabled={isEdit}
          transform={(value) =>
            value
              .toLowerCase()
              .replace(/\s+/g, "-")
          }
        />

        <ControlledSelect
          form={form}
          name="organizationType"
          label="Organization Type"
          placeholder="Select organization type"
          options={resolvedOrganizationTypeOptions}
          required
        />

        <ControlledSelect
          form={form}
          name="category"
          label="Category"
          placeholder="Select category"
          options={resolvedCategoryOptions}
          required
        />

        <ControlledSelect
          form={form}
          name="size"
          label="Organization Size"
          placeholder="Select organization size"
          options={resolvedSizeOptions}
          required
        />

        {isEdit && (
          <ControlledSelect
            form={form}
            name="status"
            label="Status"
            placeholder="Select status"
            options={organizationStatusOptions}
            required
          />
        )}

        <ControlledSelect
          form={form}
          name="timezone"
          label="Timezone"
          placeholder="Select timezone"
          options={timezoneOptions}
          required
        />

        <ControlledSwitch
          form={form}
          name="isDemo"
          label="Demo Organization"
          description="Mark this organization as a demo organization."
        />
      </FormGrid>
    </FormSection>
  );
}
