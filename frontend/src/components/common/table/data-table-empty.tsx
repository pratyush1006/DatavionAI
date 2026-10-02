/**
 * Enterprise data table empty state.
 */

"use client";

import type { ReactNode } from "react";

import { Database } from "lucide-react";

import { cn } from "@/lib/utils";

export type DataTableEmptyProps = Readonly<{
  title?: string;

  description?: string;

  icon?: ReactNode;

  action?: ReactNode;

  className?: string;
}>;

export function DataTableEmpty({
  title = "No data found",
  description = "There are no records to display.",
  icon,
  action,
  className,
}: DataTableEmptyProps) {
  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center rounded-lg border border-dashed border-border bg-muted/20 px-6 py-16 text-center",
        className,
      )}
    >
      <div className="mb-4 rounded-full bg-muted p-4 text-muted-foreground">
        {icon ?? (
          <Database className="size-8" />
        )}
      </div>

      <h3 className="text-lg font-semibold">
        {title}
      </h3>

      <p className="mt-2 max-w-md text-sm text-muted-foreground">
        {description}
      </p>

      {action && (
        <div className="mt-6">
          {action}
        </div>
      )}
    </div>
  );
}
