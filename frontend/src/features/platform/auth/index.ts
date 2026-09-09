/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/auth/index.ts
 * =============================================================================
 *
 * Public entry point for the platform authentication feature.
 * =============================================================================
 */

/* =============================================================================
 * Components
 * =============================================================================
 */

export {
  LoginForm,
} from "./components/forms/login-form";

export {
  LoginFields,
} from "./components/forms/login-fields";

export {
  LoginActions,
} from "./components/forms/login-actions";

export {
  ForgotPasswordForm,
} from "./components/forms/forgot-password-form";

export {
  ResetPasswordForm,
} from "./components/forms/reset-password-form";

/* =============================================================================
 * Domain
 * =============================================================================
 */

export {
  forgotPasswordSchema,
  loginSchema,
  resetPasswordSchema,
} from "./domain/schema";

export type {
  ForgotPasswordFormValues,
  LoginFormValues,
  ResetPasswordFormValues,
} from "./domain/schema";

/* =============================================================================
 * Pages
 * =============================================================================
 */

export {
  LoginPage,
} from "./pages/login-page";

export {
  ForgotPasswordPage,
} from "./pages/forgot-password-page";
