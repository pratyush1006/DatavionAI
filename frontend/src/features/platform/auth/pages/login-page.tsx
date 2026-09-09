/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/auth/pages/login-page.tsx
 * =============================================================================
 *
 * Login page.
 *
 * Authentication flow:
 *
 *   1. Email + password
 *   2. Login OTP
 *   3. JWT authentication
 *   4. Current-user resolution
 *   5. Dashboard navigation
 *
 * Authentication state is owned by the canonical core authentication runtime.
 *
 * Contextual action feedback is rendered next to the action that produced it.
 * Global toast notifications are intentionally not used for this flow.
 * =============================================================================
 */

"use client";

import {
  useState,
} from "react";

import {
  useRouter,
} from "next/navigation";

import {
  ActionFeedback,
} from "@/components/common/feedback";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import {
  useAuth,
} from "@/core/auth";

import {
  ApiClientError,
} from "@/core/api/client";

import {
  API_ERROR_CODES,
} from "@/core/api/errors";

import {
  LoginForm,
} from "../components/forms/login-form";

import type {
  LoginFormValues,
} from "../domain/schema";

/* =============================================================================
 * Constants
 * =============================================================================
 */

const LOGIN_CREDENTIAL_ERROR =
  "Invalid email or password.";

const LOGIN_TIMEOUT_ERROR =
  "The login request timed out. Please try again.";

const LOGIN_CANCELLED_ERROR =
  "The login request was cancelled. Please try again.";

const LOGIN_NETWORK_ERROR =
  "Unable to reach the authentication service. Please try again.";

const LOGIN_GENERIC_ERROR =
  "Unable to complete sign in. Please try again.";

const OTP_INVALID_ERROR =
  "Invalid or expired verification code.";

const OTP_TIMEOUT_ERROR =
  "The verification request timed out. Please try again.";

const OTP_CANCELLED_ERROR =
  "The verification request was cancelled. Please try again.";

const OTP_NETWORK_ERROR =
  "Unable to reach the authentication service. Please try again.";

const OTP_GENERIC_ERROR =
  "Unable to verify the login code. Please try again.";

const DASHBOARD_PATH =
  "/dashboard";

const SUCCESS_NAVIGATION_DELAY_MS =
  800;

/* =============================================================================
 * Error Helpers
 * =============================================================================
 */

/**
 * Convert an authentication request error into a safe contextual message.
 *
 * Credential failures are deliberately kept generic.
 *
 * Transport failures are never presented as credential failures because a
 * timeout, cancellation, or network failure does not prove that credentials
 * were invalid.
 */
function getLoginRequestErrorMessage(
  error: unknown,
): string {
  if (
    error instanceof ApiClientError
  ) {
    switch (error.code) {
      case API_ERROR_CODES.UNAUTHENTICATED:
        return LOGIN_CREDENTIAL_ERROR;

      case API_ERROR_CODES.REQUEST_TIMEOUT:
        return LOGIN_TIMEOUT_ERROR;

      case API_ERROR_CODES.REQUEST_CANCELLED:
        return LOGIN_CANCELLED_ERROR;

      case API_ERROR_CODES.NETWORK_ERROR:
        return LOGIN_NETWORK_ERROR;

      case API_ERROR_CODES.BAD_REQUEST:
        return (
          error.message ||
          "The login request is invalid."
        );

      case API_ERROR_CODES.RATE_LIMIT_EXCEEDED:
        return (
          error.message ||
          "Too many login attempts. Please try again later."
        );

      default:
        return (
          error.message ||
          LOGIN_GENERIC_ERROR
        );
    }
  }

  if (
    error instanceof Error &&
    error.message.trim()
  ) {
    return error.message;
  }

  return LOGIN_GENERIC_ERROR;
}

/**
 * Convert an OTP verification error into a safe contextual message.
 *
 * A verification failure is only described as an invalid/expired OTP when
 * the error actually represents an authentication failure. Transport errors
 * remain transport errors.
 */
function getOtpVerificationErrorMessage(
  error: unknown,
): string {
  if (
    error instanceof ApiClientError
  ) {
    switch (error.code) {
      case API_ERROR_CODES.UNAUTHENTICATED:
        return OTP_INVALID_ERROR;

      case API_ERROR_CODES.REQUEST_TIMEOUT:
        return OTP_TIMEOUT_ERROR;

      case API_ERROR_CODES.REQUEST_CANCELLED:
        return OTP_CANCELLED_ERROR;

      case API_ERROR_CODES.NETWORK_ERROR:
        return OTP_NETWORK_ERROR;

      case API_ERROR_CODES.BAD_REQUEST:
        return (
          error.message ||
          OTP_INVALID_ERROR
        );

      case API_ERROR_CODES.RATE_LIMIT_EXCEEDED:
        return (
          error.message ||
          "Too many verification attempts. Please try again later."
        );

      default:
        return (
          error.message ||
          OTP_GENERIC_ERROR
        );
    }
  }

  if (
    error instanceof Error &&
    error.message.trim()
  ) {
    return error.message;
  }

  return OTP_GENERIC_ERROR;
}

/* =============================================================================
 * Page
 * =============================================================================
 */

export function LoginPage() {
  const router =
    useRouter();

  const {
    requestLoginOTP,
    verifyLoginOTP,
    isAuthenticated,
    isInitialized,
  } = useAuth();

  /*
   * Active OTP session.
   *
   * When this value exists, the OTP verification screen is rendered.
   */
  const [
    otpId,
    setOtpId,
  ] = useState<
    string | null
  >(null);

  /*
   * OTP session received from the API but not yet opened.
   *
   * Keeping this separate from otpId allows the OTP-request success message
   * to remain visible until the user explicitly continues.
   */
  const [
    pendingOtpId,
    setPendingOtpId,
  ] = useState<
    string | null
  >(null);

  const [
    otp,
    setOtp,
  ] = useState("");

  const [
    loginEmail,
    setLoginEmail,
  ] = useState("");

  const [
    isSubmitting,
    setIsSubmitting,
  ] = useState(false);

  const [
    isVerifyingOtp,
    setIsVerifyingOtp,
  ] = useState(false);

  const [
    loginError,
    setLoginError,
  ] = useState<
    string | null
  >(null);

  const [
    otpRequestSuccess,
    setOtpRequestSuccess,
  ] = useState<
    string | null
  >(null);

  const [
    otpError,
    setOtpError,
  ] = useState<
    string | null
  >(null);

  const [
    welcomeMessage,
    setWelcomeMessage,
  ] = useState<
    string | null
  >(null);

  /* ===========================================================================
   * Login / OTP Request
   * =========================================================================== */

  async function handleSubmit(
    values: LoginFormValues,
  ): Promise<void> {
    if (isSubmitting) {
      return;
    }

    setLoginError(null);
    setOtpRequestSuccess(null);
    setPendingOtpId(null);

    try {
      setIsSubmitting(true);

      const response =
        await requestLoginOTP(
          values,
        );

      setLoginEmail(
        values.email.trim(),
      );

      setOtp("");

      /*
       * Store the OTP session without opening the OTP screen.
       *
       * This is intentional: the user must be able to read the success
       * message before continuing.
       */
      setPendingOtpId(
        response.otp_id,
      );

      setOtpRequestSuccess(
        "Verification code sent to your email.",
      );
    } catch (error) {
      console.error(
        "Login request failed:",
        error,
      );

      setLoginError(
        getLoginRequestErrorMessage(
          error,
        ),
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  /* ===========================================================================
   * Continue To OTP
   * =========================================================================== */

  function handleContinueToOtp(): void {
    if (
      !pendingOtpId ||
      isSubmitting
    ) {
      return;
    }

    setOtpId(
      pendingOtpId,
    );

    setPendingOtpId(null);
    setOtpRequestSuccess(null);
    setLoginError(null);
    setOtpError(null);
    setWelcomeMessage(null);
  }

  /* ===========================================================================
   * OTP Verification
   * =========================================================================== */

  async function handleVerifyOtp(): Promise<void> {
    if (isVerifyingOtp) {
      return;
    }

    setOtpError(null);
    setWelcomeMessage(null);

    if (!otpId) {
      setOtpError(
        "Login verification session is missing.",
      );

      return;
    }

    const normalizedOtp =
      otp.trim();

    if (!normalizedOtp) {
      setOtpError(
        "Please enter the verification code.",
      );

      return;
    }

    if (
      normalizedOtp.length !== 6
    ) {
      setOtpError(
        "Please enter the 6-digit verification code.",
      );

      return;
    }

    try {
      setIsVerifyingOtp(true);

      /*
       * AuthProvider performs the complete authentication transaction:
       *
       *   verify OTP
       *        ↓
       *   save access/refresh tokens
       *        ↓
       *   GET /auth/me/
       *        ↓
       *   publish authenticated user
       */
      const session =
        await verifyLoginOTP({
          otp_id: otpId,
          otp: normalizedOtp,
        });

      /*
       * The returned session is the authoritative result of this operation.
       *
       * Do not depend on isAuthenticated here because React/store subscription
       * updates are not guaranteed to be synchronously reflected in the same
       * render.
       */
      if (
        !session?.user
      ) {
        setOtpError(
          "Login completed, but your user session could not be loaded.",
        );

        return;
      }

      setWelcomeMessage(
        "Welcome to Datavion AI.",
      );

      /*
       * Authentication itself has already completed successfully.
       *
       * Keep the success feedback visible briefly before navigation.
       */
      window.setTimeout(
        () => {
          router.replace(
            DASHBOARD_PATH,
          );
        },
        SUCCESS_NAVIGATION_DELAY_MS,
      );
    } catch (error) {
      console.error(
        "Login OTP verification failed:",
        error,
      );

      setOtpError(
        getOtpVerificationErrorMessage(
          error,
        ),
      );
    } finally {
      setIsVerifyingOtp(false);
    }
  }

  /* ===========================================================================
   * Already Authenticated
   * =========================================================================== */

  if (
    isInitialized &&
    isAuthenticated
  ) {
    return (
      <main className="flex min-h-screen items-center justify-center">
        <div className="text-sm text-muted-foreground">
          Opening your dashboard...
        </div>
      </main>
    );
  }

  /* ===========================================================================
   * OTP Screen
   * =========================================================================== */

  if (otpId) {
    return (
      <main className="flex min-h-screen items-center justify-center">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle>
              Verify your login
            </CardTitle>
          </CardHeader>

          <CardContent className="space-y-6">
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">
                We sent a verification code to:
              </p>

              <p className="font-medium">
                {loginEmail}
              </p>
            </div>

            <div className="space-y-2">
              <label
                htmlFor="login-otp"
                className="text-sm font-medium"
              >
                Verification code
              </label>

              <input
                id="login-otp"
                type="text"
                inputMode="numeric"
                autoComplete="one-time-code"
                maxLength={6}
                value={otp}
                onChange={(event) => {
                  const value =
                    event.target.value
                      .replace(/\D/g, "")
                      .slice(0, 6);

                  setOtp(value);

                  if (otpError) {
                    setOtpError(null);
                  }
                }}
                placeholder="Enter OTP"
                className="w-full rounded-md border px-3 py-2 text-center tracking-[0.35em]"
                disabled={
                  isVerifyingOtp
                }
                autoFocus
              />
            </div>

            <div>
              <button
                type="button"
                onClick={
                  handleVerifyOtp
                }
                disabled={
                  isVerifyingOtp ||
                  otp.length !== 6
                }
                className="w-full rounded-md bg-black px-4 py-2 text-white disabled:cursor-not-allowed disabled:opacity-50"
              >
                {isVerifyingOtp
                  ? "Verifying..."
                  : "Verify & Sign In"}
              </button>

              <ActionFeedback
                successMessage={
                  welcomeMessage
                }
                errorMessage={
                  otpError
                }
              />
            </div>

            <button
              type="button"
              onClick={() => {
                if (
                  isVerifyingOtp
                ) {
                  return;
                }

                setOtpId(null);
                setPendingOtpId(null);
                setOtp("");
                setOtpError(null);
                setWelcomeMessage(null);
                setOtpRequestSuccess(null);
                setLoginError(null);
              }}
              disabled={
                isVerifyingOtp
              }
              className="w-full text-sm text-muted-foreground hover:underline"
            >
              Back to sign in
            </button>
          </CardContent>
        </Card>
      </main>
    );
  }

  /* ===========================================================================
   * Credentials Screen
   * =========================================================================== */

  return (
    <main className="flex min-h-screen items-center justify-center">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>
            Sign in
          </CardTitle>
        </CardHeader>

        <CardContent>
          <LoginForm
            isSubmitting={
              isSubmitting
            }
            successMessage={
              otpRequestSuccess
            }
            errorMessage={
              loginError
            }
            onSubmit={
              handleSubmit
            }
          />

          {pendingOtpId ? (
            <div className="pt-3">
              <button
                type="button"
                onClick={
                  handleContinueToOtp
                }
                className="w-full rounded-md border px-4 py-2 text-sm font-medium hover:bg-muted"
              >
                Continue to verification
              </button>
            </div>
          ) : null}
        </CardContent>
      </Card>
    </main>
  );
}
