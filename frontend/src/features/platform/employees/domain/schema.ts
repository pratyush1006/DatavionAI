/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/employees/domain/schema.ts
 * =============================================================================
 *
 * Employee validation schemas.
 * =============================================================================
 */

import { z } from "zod";

import {
  EMPLOYMENT_TYPES,
} from "./constants";

export const employeeSchema =
  z.object({
    organization: z
      .string()
      .trim()
      .min(
        1,
        "Organization is required.",
      ),

    user: z
      .string()
      .trim()
      .optional()
      .or(z.literal("")),

    employeeCode: z
      .string()
      .trim()
      .min(
        1,
        "Employee code is required.",
      )
      .max(
        50,
        "Employee code cannot exceed 50 characters.",
      )
      .transform((value) =>
        value.toUpperCase(),
      ),

    designation: z
      .string()
      .trim()
      .min(
        1,
        "Designation is required.",
      )
      .max(
        150,
        "Designation cannot exceed 150 characters.",
      ),

    workEmail: z
      .string()
      .trim()
      .email(
        "Enter a valid work email address.",
      )
      .optional()
      .or(z.literal("")),

    phoneNumber: z
      .string()
      .trim()
      .max(
        30,
        "Phone number cannot exceed 30 characters.",
      )
      .optional()
      .or(z.literal("")),

    employmentType:
      z.enum(
        EMPLOYMENT_TYPES,
      ),

    joiningDate: z
      .string()
      .min(
        1,
        "Joining date is required.",
      ),
  });

export type EmployeeFormValues =
  z.infer<
    typeof employeeSchema
  >;
