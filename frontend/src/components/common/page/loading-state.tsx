/**
 * ----------------------------------------------------------------------
 * Loading State
 * ----------------------------------------------------------------------
 *
 * Purpose:
 * Displays a reusable loading placeholder for page content.
 *
 * Used By:
 * - Organizations
 * - Departments
 * - Teams
 * - Users
 * - Patients
 * - Laboratories
 *
 * ----------------------------------------------------------------------
 */

"use client";

import { Loader2 } from "lucide-react";

import { cn } from "@/lib/utils";

export type LoadingStateProps = Readonly<{
  title?: string;

  description?: string;

  className?: string;
}>;

export function LoadingState({
  title = "Loading...",
  description = "Please wait while we load your data.",
  className,
}: LoadingStateProps) {
  return (
    <div
      className={cn(
        "flex min-h-[320px] flex-col items-center justify-center rounded-xl border bg-card px-8 py-12 text-center",
        className,
      )}
    >
      <Loader2 className="h-10 w-10 animate-spin text-primary" />

      <h3 className="mt-6 text-lg font-semibold">
        {title}
      </h3>

      <p className="mt-2 max-w-md text-sm text-muted-foreground">
        {description}
      </p>
    </div>
  );
}
