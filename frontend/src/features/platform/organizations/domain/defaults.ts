/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/organizations/domain/defaults.ts
 * =============================================================================
 */

import type {
  OrganizationFormValues,
} from "./schema";

export const organizationDefaults:
  OrganizationFormValues = {
  name: "",
  displayName: "",
  code: "",
  slug: "",

  category:
    "healthcare_provider",

  organizationType:
    "hospital",

  size: "small",

  status: "active",

  email: "",

  supportEmail: "",

  phone: "",

  website: "",

  address: "",

  city: "",

  state: "",

  country: "India",

  countryRef: null,

  regionRef: null,

  cityRef: null,

  postalCode: "",

  timezone:
    "Asia/Kolkata",

  registrationNumber: "",

  taxNumber: "",

  licenseNumber: "",

  accreditation: "",

  description: "",

  isDemo: false,
};
