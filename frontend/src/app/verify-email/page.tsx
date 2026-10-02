"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useState, Suspense } from "react";

import {
  resendSignupEmailOtp,
  verifySignupEmail,
} from "@/lib/backend/self-service-signup";

function VerifyEmailPageClient() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [email, setEmail] = useState(searchParams.get("email") ?? "");
  const [otp, setOtp] = useState("");
  const [busy, setBusy] = useState(false);
  const [resending, setResending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  async function verify() {
    if (!email || !otp) {
      setError("Email and verification code are required.");
      return;
    }

    setBusy(true);
    setError(null);
    setMessage(null);

    try {
      await verifySignupEmail(email, otp);
      setMessage("Email verified successfully. Continue to login.");
      window.setTimeout(() => {
        router.replace(`/login?verified=1&email=${encodeURIComponent(email)}`);
      }, 700);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Email verification failed.");
    } finally {
      setBusy(false);
    }
  }

  async function resend() {
    if (!email) {
      setError("Enter your email address first.");
      return;
    }

    setResending(true);
    setError(null);
    setMessage(null);

    try {
      await resendSignupEmailOtp(email);
      setMessage("A new verification code has been sent.");
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Unable to resend verification code.");
    } finally {
      setResending(false);
    }
  }

  return (
    <main className="min-vh-100 d-flex align-items-center bg-body-tertiary py-5">
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-12 col-md-7 col-lg-5">
            <div className="card border-0 shadow-sm">
              <div className="card-body p-4 p-lg-5">
                <div className="small text-uppercase fw-semibold text-body-secondary mb-2">DatavionOS</div>
                <h1 className="h2 fw-bold">Verify your email</h1>
                <p className="text-body-secondary">Enter the OTP sent to your signup email.</p>

                {error ? <div className="alert alert-danger">{error}</div> : null}
                {message ? <div className="alert alert-success">{message}</div> : null}

                <div className="mb-3">
                  <label className="form-label">Email</label>
                  <input
                    type="email"
                    className="form-control"
                    aria-label="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                </div>

                <div className="mb-4">
                  <label className="form-label">Verification code</label>
                  <input
                    inputMode="numeric"
                    autoComplete="one-time-code"
                    maxLength={6}
                    className="form-control form-control-lg text-center"
                    aria-label="Verification code"
                    value={otp}
                    onChange={(e) => setOtp(e.target.value.replace(/\D/g, "").slice(0, 6))}
                  />
                </div>

                <button className="btn btn-primary btn-lg w-100" type="button" disabled={busy} onClick={() => void verify()}>
                  {busy ? "Verifying..." : "Verify email"}
                </button>

                <button className="btn btn-link w-100 mt-2" type="button" disabled={resending} onClick={() => void resend()}>
                  {resending ? "Sending..." : "Resend verification code"}
                </button>

                <div className="text-center mt-3">
                  <Link href="/login">Back to login</Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}

// VERIFY_EMAIL_PAGE_SUSPENSE_BOUNDARY
export default function VerifyEmailPage() {
  return (
    <Suspense
      fallback={
        <main className="min-vh-100 d-flex align-items-center justify-content-center">
          <div className="text-body-secondary">Loading verification...</div>
        </main>
      }
    >
      <VerifyEmailPageClient />
    </Suspense>
  );
}
