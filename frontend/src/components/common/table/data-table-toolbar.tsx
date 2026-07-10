/**
 * Enterprise data table toolbar.
 */

"use client";

import type {
  ReactNode,
} from "react";

import { cn } from "@/lib/utils";

export type DataTableToolbarProps = Readonly<{
  search?: ReactNode;

  filters?: ReactNode;

  actions?: ReactNode;

  className?: string;
}>;

export function DataTableToolbar({
  search,
  filters,
  actions,
  className,
}: DataTableToolbarProps) {
  return (
    <div
      className={cn(
        "flex flex-col gap-4 rounded-lg border border-border bg-card p-4 lg:flex-row lg:items-center lg:justify-between",
        className,
      )}
    >
      <div className="flex flex-1 flex-wrap items-center gap-3">
        {search}

        {filters}
      </div>

      {actions && (
        <div className="flex items-center gap-2">
          {actions}
        </div>
      )}
    </div>
  );
}
