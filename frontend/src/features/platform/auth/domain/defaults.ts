/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/auth/domain/defaults.ts
 * =============================================================================
 *
 * Default authentication form values.
 * =============================================================================
 */

import type {
  ForgotPasswordFormValues,
  LoginFormValues,
  ResetPasswordFormValues,
} from "./schema";

/* =============================================================================
 * Login
 * =============================================================================
 */

export const loginDefaults:
  LoginFormValues = {
  email: "",
  password: "",
};

/* =============================================================================
 * Forgot Password
 * =============================================================================
 */

export const forgotPasswordDefaults:
  ForgotPasswordFormValues = {
  email: "",
};

/* =============================================================================
 * Reset Password
 * =============================================================================
 */

export const resetPasswordDefaults:
  ResetPasswordFormValues = {
  otp: "",
  new_password: "",
  confirm_password: "",
};
