/**
 * Default organization form values.
 */

import type {
  OrganizationFormValues,
} from "./schema";

export const organizationDefaults: OrganizationFormValues =
  {
    name: "",

    code: "",

    organizationType:
      "HOSPITAL",

    email: "",

    phone: "",

    address: "",

    city: "",

    state: "",

    country: "India",

    isActive: true,
  };
