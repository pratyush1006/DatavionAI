"use client";

import { useEffect } from "react";

import { Button } from "@/components/ui/button";

export default function ErrorPage({
  error,
  reset,
}: Readonly<{
  error: Error & { digest?: string };
  reset: () => void;
}>) {
  useEffect(() => {
    // Production telemetry is intentionally added at this boundary only.
    console.error("Unhandled application error", error);
  }, [error]);

  return (
    <main className="flex min-h-screen items-center justify-center p-6">
      <section className="max-w-md space-y-4 text-center">
        <h1 className="text-2xl font-semibold">
          Something went wrong
        </h1>

        <p className="text-sm text-muted-foreground">
          Your data has not been changed. Please try again, or contact support
          if the issue continues.
        </p>

        <Button onClick={reset}>
          Try again
        </Button>
      </section>
    </main>
  );
}
