import { z } from "zod";

export const organizationSchema = z.object({
  name: z
    .string()
    .trim()
    .min(
      3,
      "Organization name must contain at least 3 characters.",
    )
    .max(
      100,
      "Organization name cannot exceed 100 characters.",
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
      "Only uppercase letters, numbers, '-' and '_' are allowed.",
    ),

  organizationType: z.enum([
    "HOSPITAL",
    "CLINIC",
    "LABORATORY",
    "RADIOLOGY",
    "PHARMACY",
    "BLOOD_BANK",
    "CORPORATE",
  ]),

  email: z
    .string()
    .email("Enter a valid email address.")
    .or(z.literal("")),

  phone: z
    .string()
    .trim()
    .min(
      5,
      "Phone number is required.",
    )
    .max(
      20,
      "Phone number is too long.",
    ),

  address: z
    .string()
    .trim()
    .min(
      5,
      "Address is required.",
    )
    .max(
      250,
      "Address cannot exceed 250 characters.",
    ),

  city: z
    .string()
    .trim()
    .min(
      2,
      "City is required.",
    )
    .max(100),

  state: z
    .string()
    .trim()
    .min(
      2,
      "State is required.",
    )
    .max(100),

  country: z
    .string()
    .trim()
    .min(
      2,
      "Country is required.",
    )
    .max(100),

  isActive: z.boolean(),
});

export type OrganizationFormValues =
  z.infer<typeof organizationSchema>;
