"use client";

import Link from "next/link";
import { Suspense } from "react";
import { useSearchParams } from "next/navigation";

function RegistrationSuccessContent() {
  const searchParams = useSearchParams();
  const email = searchParams.get("email") ?? "";
  const organization = searchParams.get("organization") ?? "your organization";
  const verificationRequired = searchParams.get("verification") === "required";

  const verifyUrl = new URLSearchParams({ email });

  return (
    <main className="container py-5">
      <div className="row justify-content-center">
        <div className="col-12 col-lg-7">
          <div className="card border-0 shadow-sm text-center">
            <div className="card-body p-5">
              <div className="display-5 text-success mb-3" aria-hidden="true">✓</div>
              <h1 className="h2">Organization registration submitted</h1>
              <p className="text-secondary">
                {organization} was submitted to DatavionOS. Provisioning,
                subscription entitlements, and organization capabilities remain
                controlled by the backend.
              </p>
              {verificationRequired ? (
                <>
                  <p className="text-secondary">
                    Verify the owner account{email ? ` sent to ${email}` : ""} to continue.
                  </p>
                  <Link href={`/verify-email?${verifyUrl.toString()}`} className="btn btn-primary px-4">
                    Verify email
                  </Link>
                </>
              ) : (
                <Link href="/login" className="btn btn-primary px-4">
                  Continue to login
                </Link>
              )}
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}

export default function RegistrationSuccessPage() {
  return (
    <Suspense fallback={<main className="container py-5">Loading registration status…</main>}>
      <RegistrationSuccessContent />
    </Suspense>
  );
}
