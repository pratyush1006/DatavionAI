/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/auth/domain/schema.ts
 * =============================================================================
 *
 * Authentication form validation schemas.
 *
 * The backend remains authoritative for authentication and password-policy
 * enforcement. These schemas provide immediate client-side validation only.
 * =============================================================================
 */

import { z } from "zod";

/* =============================================================================
 * Shared Password Validation
 * =============================================================================
 */

const passwordSchema = z
  .string()
  .min(
    1,
    "Password is required.",
  )
  .max(
    128,
    "Password is too long.",
  );

/* =============================================================================
 * Login
 * =============================================================================
 */

export const loginSchema = z.object({
  email: z
    .string()
    .trim()
    .min(
      1,
      "Email is required.",
    )
    .email(
      "Enter a valid email address.",
    ),

  password: passwordSchema,
});

export type LoginFormValues =
  z.infer<typeof loginSchema>;

/* =============================================================================
 * Forgot Password
 * =============================================================================
 */

export const forgotPasswordSchema =
  z.object({
    email: z
      .string()
      .trim()
      .min(
        1,
        "Email is required.",
      )
      .email(
        "Enter a valid email address.",
      ),
  });

export type ForgotPasswordFormValues =
  z.infer<
    typeof forgotPasswordSchema
  >;

/* =============================================================================
 * Reset Password
 * =============================================================================
 */

export const resetPasswordSchema =
  z
    .object({
      otp: z
        .string()
        .trim()
        .regex(
          /^\d{6}$/,
          "Enter the 6-digit verification code.",
        ),

      new_password: passwordSchema,

      confirm_password: z
        .string()
        .min(
          1,
          "Please confirm your password.",
        ),
    })
    .refine(
      (values) =>
        values.new_password ===
        values.confirm_password,
      {
        path: [
          "confirm_password",
        ],
        message:
          "Passwords do not match.",
      },
    );

export type ResetPasswordFormValues =
  z.infer<
    typeof resetPasswordSchema
  >;
