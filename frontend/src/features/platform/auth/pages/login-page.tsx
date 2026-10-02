"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { toast } from "sonner";

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
  resendLoginOtp,
} from "@/lib/backend/auth";

import { LoginForm } from "../components/forms/login-form";
import type { LoginFormValues } from "../domain/schema";

export function LoginPage() {
  const router = useRouter();
  const { requestLoginOTP, verifyLoginOTP } = useAuth();
  const [otpId, setOtpId] = useState<string | null>(null);
  const [otp, setOtp] = useState("");
  const [loginEmail, setLoginEmail] = useState("");
  const [loginError, setLoginError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isVerifyingOtp, setIsVerifyingOtp] = useState(false);
  const [isResendingOtp, setIsResendingOtp] = useState(false);

  async function handleSubmit(values: LoginFormValues): Promise<void> {
    if (isSubmitting) return;

    setLoginError(null);
    try {
      setIsSubmitting(true);
      setLoginEmail(values.email.trim());
      const response = await requestLoginOTP({
        email: values.email.trim(),
        password: values.password,
      });

      const requiresOtp =
        response.requires_otp === true ||
        response.requires_otp === "True";
      if (!requiresOtp || !response.otp_id) {
        const message = "The authentication service did not return a valid OTP challenge.";
        setLoginError(message);
        toast.error(message);
        return;
      }

      setLoginEmail(values.email);
      setOtpId(response.otp_id);
      setOtp("");
      toast.success("Verification code sent to your email.");
    } catch (error) {
      console.error("Login request failed:", error);
      const message = error instanceof Error ? error.message : "Invalid email or password.";
      setLoginError(message);
      toast.error(message);
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleVerifyOtp(): Promise<void> {
    if (isVerifyingOtp || !otpId) return;

    const normalizedOtp = otp.trim();
    if (normalizedOtp.length !== 6) {
      toast.error("Please enter the 6-digit verification code.");
      return;
    }

    try {
      setIsVerifyingOtp(true);
      await verifyLoginOTP({
        otp_id: otpId,
        otp: normalizedOtp,
      });
      toast.success("Welcome to Datavion AI.");
      router.replace("/dashboard");
      router.refresh();
    } catch (error) {
      console.error("Login OTP verification failed:", error);
      toast.error(error instanceof Error ? error.message : "Invalid or expired verification code.");
    } finally {
      setIsVerifyingOtp(false);
    }
  }

  async function handleResendOtp(): Promise<void> {
    if (isResendingOtp || !otpId) return;

    try {
      setIsResendingOtp(true);
      const response = await resendLoginOtp(otpId);
      if (!response.otp_id) {
        toast.error("The authentication service did not return a new OTP challenge.");
        return;
      }
      setOtpId(response.otp_id);
      setOtp("");
      toast.success("A new verification code has been sent.");
    } catch (error) {
      console.error("Login OTP resend failed:", error);
      toast.error(error instanceof Error ? error.message : "Unable to resend the verification code.");
    } finally {
      setIsResendingOtp(false);
    }
  }

  if (otpId) {
    return (
      <main className="flex min-h-screen items-center justify-center">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle>Verify your login</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">We sent a verification code to:</p>
              <p className="font-medium">{loginEmail}</p>
            </div>
            <div className="space-y-2">
              <label htmlFor="login-otp" className="text-sm font-medium">Verification code</label>
              <input
                id="login-otp"
                type="text"
                inputMode="numeric"
                autoComplete="one-time-code"
                maxLength={6}
                value={otp}
                onChange={(event) => setOtp(event.target.value.replace(/\D/g, "").slice(0, 6))}
                placeholder="Enter OTP"
                className="w-full rounded-md border px-3 py-2 text-center tracking-[0.35em]"
                disabled={isVerifyingOtp || isResendingOtp}
                autoFocus
              />
            </div>
            <button
              type="button"
              onClick={handleVerifyOtp}
              disabled={isVerifyingOtp || isResendingOtp || otp.length !== 6}
              className="w-full rounded-md bg-black px-4 py-2 text-white disabled:cursor-not-allowed disabled:opacity-50"
            >
              {isVerifyingOtp ? "Verifying..." : "Verify & Sign In"}
            </button>
            <button
              type="button"
              onClick={handleResendOtp}
              disabled={isVerifyingOtp || isResendingOtp}
              className="w-full text-sm text-primary hover:underline disabled:opacity-50"
            >
              {isResendingOtp ? "Resending..." : "Resend verification code"}
            </button>
            <button
              type="button"
              onClick={() => {
                if (isVerifyingOtp || isResendingOtp) return;
                setOtpId(null);
                setOtp("");
              }}
              className="w-full text-sm text-muted-foreground hover:underline"
              disabled={isVerifyingOtp || isResendingOtp}
            >
              Back to sign in
            </button>
          </CardContent>
        </Card>
      </main>
    );
  }

  return (
    <main className="flex min-h-screen items-center justify-center">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Sign in</CardTitle>
        </CardHeader>
        <CardContent>
          {loginError ? (
            <div className="mb-4 rounded-md border border-destructive/30 bg-destructive/5 p-3 text-sm" role="alert">
              <p className="mb-0">{loginError}</p>
              {loginError.toLowerCase().includes("verify your email") ? (
                <Link
                  className="mt-2 inline-block font-medium text-primary underline-offset-4 hover:underline"
                  href={`/verify-email?email=${encodeURIComponent(loginEmail)}`}
                >
                  Verify your email
                </Link>
              ) : null}
            </div>
          ) : null}
          <LoginForm isSubmitting={isSubmitting} onSubmit={handleSubmit} />
          <div className="mt-4 text-right text-sm">
            <Link className="text-primary underline-offset-4 hover:underline" href="/forgot-password">
              Forgot password?
            </Link>
          </div>
        </CardContent>
      </Card>
    </main>
  );
}
