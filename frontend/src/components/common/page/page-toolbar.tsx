/**
 * Enterprise page toolbar.
 */

import type { ReactNode } from "react";

import { cn } from "@/lib/utils";

export type PageToolbarProps = Readonly<{
  search?: ReactNode;

  filters?: ReactNode;

  actions?: ReactNode;

  className?: string;
}>;

export function PageToolbar({
  search,
  filters,
  actions,
  className,
}: PageToolbarProps) {
  return (
    <div
      className={cn(
        "flex flex-col gap-4 rounded-xl border bg-card p-4",
        "lg:flex-row lg:items-center lg:justify-between",
        className,
      )}
    >
      <div className="flex flex-1 flex-col gap-4 lg:flex-row lg:items-center">
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
