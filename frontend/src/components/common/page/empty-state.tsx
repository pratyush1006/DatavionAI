/**
 * ----------------------------------------------------------------------
 * Empty State
 * ----------------------------------------------------------------------
 *
 * Purpose:
 * Displays a reusable empty state when no data is available.
 *
 * Used By:
 * - Organizations
 * - Departments
 * - Teams
 * - Users
 * - Patients
 * - Laboratories
 * - Billing
 *
 * ----------------------------------------------------------------------
 */

"use client";

import type { ReactNode } from "react";

import { Inbox } from "lucide-react";

import { cn } from "@/lib/utils";

export type EmptyStateProps = Readonly<{
  title: string;

  description?: string;

  icon?: ReactNode;

  action?: ReactNode;

  className?: string;
}>;

export function EmptyState({
  title,
  description,
  icon,
  action,
  className,
}: EmptyStateProps) {
  return (
    <div
      className={cn(
        "flex min-h-[320px] flex-col items-center justify-center rounded-xl border border-dashed bg-card px-8 py-12 text-center",
        className,
      )}
    >
      <div className="mb-6 rounded-full bg-muted p-4">
        {icon ?? (
          <Inbox className="h-8 w-8 text-muted-foreground" />
        )}
      </div>

      <h3 className="text-xl font-semibold">
        {title}
      </h3>

      {description && (
        <p className="mt-2 max-w-md text-sm text-muted-foreground">
          {description}
        </p>
      )}

      {action && (
        <div className="mt-8">
          {action}
        </div>
      )}
    </div>
  );
}
