"use client";

import { useEffect } from "react";

export default function GlobalError({
  error,
  reset,
}: Readonly<{
  error: Error & { digest?: string };
  reset: () => void;
}>) {
  useEffect(() => {
    // Keep diagnostics in the browser console without exposing internals in UI.
    console.error("DatavionOS route error", error);
  }, [error]);

  return (
    <main className="min-vh-100 d-flex align-items-center justify-content-center bg-body-tertiary p-4">
      <section className="card border-0 shadow-sm" style={{ maxWidth: 520 }}>
        <div className="card-body p-4 p-md-5 text-center">
          <h1 className="h3">We couldn&apos;t load this page</h1>
          <p className="text-body-secondary mb-4">
            Please retry. If this keeps happening, contact your organization administrator.
          </p>
          <button className="btn btn-primary" type="button" onClick={reset}>
            Retry
          </button>
        </div>
      </section>
    </main>
  );
}
