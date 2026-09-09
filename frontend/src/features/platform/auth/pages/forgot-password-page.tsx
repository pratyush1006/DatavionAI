/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/auth/pages/forgot-password-page.tsx
 * =============================================================================
 *
 * Forgot-password page.
 *
 * Authentication flow:
 *
 *   1. Enter email
 *   2. Request password-reset OTP
 *   3. Enter OTP
 *   4. Enter new password
 *   5. Reset password
 *   6. Return to login
 *
 * Authentication infrastructure remains owned by @/core/auth.
 *
 * Contextual action feedback is rendered directly below the action that
 * produced it. Global toast notifications are intentionally not used here.
 * =============================================================================
 */

"use client";

import {
  useState,
} from "react";

import Link from "next/link";

import {
  useRouter,
} from "next/navigation";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import {
  useAuth,
} from "@/core/auth";

import type {
  ForgotPasswordFormValues,
  ResetPasswordFormValues,
} from "../domain/schema";

import {
  ForgotPasswordForm,
  ResetPasswordForm,
} from "../components/forms";

/* =============================================================================
 * Types
 * =============================================================================
 */

type ResetStep =
  | "request"
  | "reset";

/* =============================================================================
 * Page
 * =============================================================================
 */

export function ForgotPasswordPage() {
  const router =
    useRouter();

  const {
    forgotPassword,
    resetPassword,
  } = useAuth();

  const [
    step,
    setStep,
  ] = useState<ResetStep>(
    "request",
  );

  const [
    email,
    setEmail,
  ] = useState("");

  /*
   * The successful request is stored independently from the visible step.
   *
   * This allows the request feedback to remain visible until the user
   * explicitly continues to the reset form.
   */
  const [
    resetSessionReady,
    setResetSessionReady,
  ] = useState(false);

  const [
    isSubmitting,
    setIsSubmitting,
  ] = useState(false);

  const [
    requestSuccess,
    setRequestSuccess,
  ] = useState<
    string | null
  >(null);

  const [
    requestError,
    setRequestError,
  ] = useState<
    string | null
  >(null);

  const [
    resetSuccess,
    setResetSuccess,
  ] = useState<
    string | null
  >(null);

  const [
    resetError,
    setResetError,
  ] = useState<
    string | null
  >(null);

  /* ===========================================================================
   * Forgot Password Request
   * =========================================================================== */

  async function handleForgotPassword(
    values: ForgotPasswordFormValues,
  ): Promise<void> {
    if (isSubmitting) {
      return;
    }

    setRequestSuccess(null);
    setRequestError(null);
    setResetSessionReady(false);

    try {
      setIsSubmitting(true);

      const normalizedEmail =
        values.email.trim();

      await forgotPassword({
        email:
          normalizedEmail,
      });

      setEmail(
        normalizedEmail,
      );

      /*
       * The request succeeded.
       *
       * Keep the request screen mounted so the user can read the message.
       */
      setRequestSuccess(
        "Verification code sent. Check your email.",
      );

      setResetSessionReady(true);
    } catch (error) {
      console.error(
        "Password reset request failed:",
        error,
      );

      /*
       * Do not expose whether an account exists.
       */
      setRequestSuccess(
        "If an account exists for that email, a verification code has been sent.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  /* ===========================================================================
   * Continue To Reset
   * =========================================================================== */

  function handleContinueToReset(): void {
    if (
      !resetSessionReady ||
      isSubmitting
    ) {
      return;
    }

    setStep("reset");
    setResetSessionReady(false);
    setRequestSuccess(null);
    setRequestError(null);
  }

  /* ===========================================================================
   * Password Reset
   * =========================================================================== */

  async function handleResetPassword(
    values: ResetPasswordFormValues,
  ): Promise<void> {
    if (isSubmitting) {
      return;
    }

    setResetSuccess(null);
    setResetError(null);

    if (!email) {
      setResetError(
        "Your password-reset session is missing. Please start again.",
      );

      setStep("request");

      return;
    }

    try {
      setIsSubmitting(true);

      await resetPassword({
        email,
        otp:
          values.otp.trim(),
        new_password:
          values.new_password,
      });

      setResetSuccess(
        "Your password has been reset successfully.",
      );

      /*
       * Password reset has completed successfully.
       *
       * Keep the contextual success feedback visible briefly before
       * returning the user to login.
       */
      window.setTimeout(
        () => {
          router.replace(
            "/login",
          );
        },
        800,
      );
    } catch (error) {
      console.error(
        "Password reset failed:",
        error,
      );

      setResetError(
        "The verification code may be invalid or expired, or the password could not be reset.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  /* ===========================================================================
   * Navigation
   * =========================================================================== */

  function handleBack(): void {
    if (isSubmitting) {
      return;
    }

    setRequestSuccess(null);
    setRequestError(null);
    setResetSuccess(null);
    setResetError(null);
    setResetSessionReady(false);

    setStep("request");
  }

  /* ===========================================================================
   * Render
   * =========================================================================== */

  return (
    <main className="flex min-h-screen items-center justify-center p-6">
      <Card className="w-full max-w-md">
        {step === "request" ? (
          <>
            <CardHeader>
              <CardTitle>
                Forgot your password?
              </CardTitle>

              <CardDescription>
                Enter your email address and
                we&apos;ll send you a verification
                code to reset your password.
              </CardDescription>
            </CardHeader>

            <CardContent>
              <ForgotPasswordForm
                isSubmitting={
                  isSubmitting
                }
                successMessage={
                  requestSuccess
                }
                errorMessage={
                  requestError
                }
                onSubmit={
                  handleForgotPassword
                }
              />

              {resetSessionReady ? (
                <div className="pt-3">
                  <button
                    type="button"
                    onClick={
                      handleContinueToReset
                    }
                    className="w-full rounded-md border px-4 py-2 text-sm font-medium hover:bg-muted"
                  >
                    Continue to reset password
                  </button>
                </div>
              ) : null}

              <div className="mt-6 text-center text-sm">
                <Link
                  href="/login"
                  className="text-muted-foreground hover:text-foreground hover:underline"
                >
                  Back to sign in
                </Link>
              </div>
            </CardContent>
          </>
        ) : (
          <>
            <CardHeader>
              <CardTitle>
                Reset your password
              </CardTitle>

              <CardDescription>
                Enter the verification code
                sent to{" "}
                <span className="font-medium text-foreground">
                  {email}
                </span>{" "}
                and choose a new password.
              </CardDescription>
            </CardHeader>

            <CardContent>
              <ResetPasswordForm
                isSubmitting={
                  isSubmitting
                }
                successMessage={
                  resetSuccess
                }
                errorMessage={
                  resetError
                }
                onSubmit={
                  handleResetPassword
                }
              />

              <div className="mt-6 flex flex-col gap-3 text-center text-sm">
                <button
                  type="button"
                  onClick={
                    handleBack
                  }
                  disabled={
                    isSubmitting
                  }
                  className="text-muted-foreground hover:text-foreground hover:underline disabled:pointer-events-none disabled:opacity-50"
                >
                  Use a different email
                </button>

                <Link
                  href="/login"
                  className="text-muted-foreground hover:text-foreground hover:underline"
                >
                  Back to sign in
                </Link>
              </div>
            </CardContent>
          </>
        )}
      </Card>
    </main>
  );
}
