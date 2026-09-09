/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/organizations/domain/schema.ts
 * =============================================================================
 *
 * Canonical organization validation schema.
 * =============================================================================
 */

import {
  z,
} from "zod";

/* =============================================================================
 * Shared Helpers
 * =============================================================================
 */

const requiredText = (
  field: string,
  min = 1,
  max = 255,
) =>
  z
    .string()
    .trim()
    .min(
      min,
      `${field} is required.`,
    )
    .max(
      max,
      `${field} cannot exceed ${max} characters.`,
    );

const optionalReference = z
  .string()
  .uuid()
  .nullable();

/* =============================================================================
 * Organization Field Shape
 * =============================================================================
 */

const organizationFields = {
  name: requiredText(
    "Organization name",
    3,
    255,
  ),

  displayName: requiredText(
    "Display name",
    2,
    255,
  ),

  code: z
    .string()
    .trim()
    .min(
      2,
      "Organization code is required.",
    )
    .max(
      20,
      "Organization code cannot exceed 20 characters.",
    )
    .regex(
      /^[A-Z0-9_-]+$/,
      "Use uppercase letters, numbers, '-' or '_'.",
    ),

  slug: z
    .string()
    .trim()
    .min(
      1,
      "Slug is required.",
    )
    .max(
      100,
      "Slug cannot exceed 100 characters.",
    )
    .regex(
      /^[a-z0-9]+(?:-[a-z0-9]+)*$/,
      "Use lowercase letters, numbers and hyphens only.",
    ),

  category: requiredText(
    "Category",
    1,
    50,
  ),

  organizationType: requiredText(
    "Organization type",
    1,
    100,
  ),

  size: requiredText(
    "Organization size",
    1,
    30,
  ),

  status: requiredText(
    "Status",
    1,
    50,
  ),

  email: z
    .string()
    .trim()
    .min(
      1,
      "Email address is required.",
    )
    .email(
      "Enter a valid email address.",
    ),

  supportEmail: z
    .string()
    .trim()
    .min(
      1,
      "Support email is required.",
    )
    .email(
      "Enter a valid support email address.",
    ),

  phone: z
    .string()
    .trim()
    .min(
      7,
      "Phone number is required.",
    )
    .max(
      20,
      "Phone number cannot exceed 20 characters.",
    )
    .regex(
      /^\+?[0-9][0-9\s().-]{6,19}$/,
      "Enter a valid phone number.",
    ),

  website: z
    .string()
    .trim()
    .url(
      "Enter a valid website URL.",
    )
    .or(
      z.literal(""),
    ),

  address: requiredText(
    "Address",
    5,
    500,
  ),

  /**
   * Legacy compatibility/display values.
   *
   * These remain synchronized with the selected Geography records.
   */
  city: requiredText(
    "City",
    2,
    100,
  ),

  state: requiredText(
    "State",
    2,
    100,
  ),

  country: requiredText(
    "Country",
    2,
    100,
  ),

  /**
   * Canonical Geography references.
   *
   * Nullable because the backend Organization model permits nullable refs,
   * while the UI requires the human-readable address fields.
   */
  countryRef: optionalReference,

  regionRef: optionalReference,

  cityRef: optionalReference,

  postalCode: requiredText(
    "Postal code",
    3,
    20,
  ),

  timezone: requiredText(
    "Timezone",
    1,
    100,
  ),

  registrationNumber: requiredText(
    "Registration number",
    2,
    100,
  ),

  taxNumber: requiredText(
    "Tax number",
    2,
    100,
  ),

  licenseNumber: requiredText(
    "License number",
    2,
    100,
  ),

  accreditation: requiredText(
    "Accreditation",
    2,
    100,
  ),

  description: requiredText(
    "Description",
    10,
    5000,
  ),

  isDemo: z.boolean(),
} as const;

/* =============================================================================
 * Category / Type Compatibility
 * =============================================================================
 */

const allowedTypes: Record<
  string,
  readonly string[]
> = {
  healthcare_provider: [
    "hospital",
    "clinic",
    "dental_clinic",
    "eye_clinic",
    "ent_clinic",
    "cardiology_clinic",
    "neurology_clinic",
    "orthopedic_clinic",
    "pediatric_clinic",
    "gynecology_clinic",
    "dermatology_clinic",
    "psychiatry_clinic",
    "oncology_center",
    "physiotherapy_center",
    "rehabilitation_center",
    "dialysis_center",
    "fertility_center",
    "home_healthcare",
    "telemedicine",
    "nursing_home",
    "hospice",
    "assisted_living",
    "wellness_center",
  ],

  diagnostics: [
    "laboratory",
    "diagnostic_center",
    "radiology_center",
    "imaging_center",
    "pathology_lab",
    "blood_bank",
  ],

  pharmacy: [
    "retail_pharmacy",
    "hospital_pharmacy",
    "online_pharmacy",
    "wholesale_pharmacy",
  ],

  emergency: [
    "ambulance_service",
    "trauma_center",
    "emergency_center",
  ],

  insurance: [
    "insurance_company",
    "tpa",
  ],

  research: [
    "medical_college",
    "medical_university",
    "research_institute",
    "clinical_trial_center",
  ],

  public_health: [
    "government_hospital",
    "public_health_center",
    "ngo",
  ],

  enterprise: [
    "corporate",
    "occupational_health",
    "healthcare_network",
  ],
};

function validateOrganizationTypeCompatibility<
  T extends {
    category: string;
    organizationType: string;
  },
>(
  values: T,
  context: z.RefinementCtx,
): void {
  const types =
    allowedTypes[
      values.category
    ];

  if (
    types &&
    !types.includes(
      values.organizationType,
    )
  ) {
    context.addIssue({
      code: "custom",
      path: [
        "organizationType",
      ],
      message:
        "Selected organization type is not valid for the chosen category.",
    });
  }
}

/* =============================================================================
 * Create Schema
 * =============================================================================
 */

export const organizationSchema =
  z
    .object(
      organizationFields,
    )
    .superRefine(
      validateOrganizationTypeCompatibility,
    );

export type OrganizationFormValues =
  z.infer<
    typeof organizationSchema
  >;

/* =============================================================================
 * Update Schema
 * =============================================================================
 */

export const organizationUpdateSchema =
  z
    .object({
      name:
        organizationFields.name,

      displayName:
        organizationFields.displayName,

      category:
        organizationFields.category,

      organizationType:
        organizationFields.organizationType,

      size:
        organizationFields.size,

      status:
        organizationFields.status,

      email:
        organizationFields.email,

      supportEmail:
        organizationFields.supportEmail,

      phone:
        organizationFields.phone,

      website:
        organizationFields.website,

      address:
        organizationFields.address,

      city:
        organizationFields.city,

      state:
        organizationFields.state,

      country:
        organizationFields.country,

      countryRef:
        organizationFields.countryRef,

      regionRef:
        organizationFields.regionRef,

      cityRef:
        organizationFields.cityRef,

      postalCode:
        organizationFields.postalCode,

      timezone:
        organizationFields.timezone,

      registrationNumber:
        organizationFields.registrationNumber,

      taxNumber:
        organizationFields.taxNumber,

      licenseNumber:
        organizationFields.licenseNumber,

      accreditation:
        organizationFields.accreditation,

      description:
        organizationFields.description,

      isDemo:
        organizationFields.isDemo,
    })
    .superRefine(
      validateOrganizationTypeCompatibility,
    );

export type OrganizationUpdateFormValues =
  z.infer<
    typeof organizationUpdateSchema
  >;
