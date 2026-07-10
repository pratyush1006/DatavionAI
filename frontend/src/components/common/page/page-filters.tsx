/**
 * Enterprise page filters container.
 */

import type { ReactNode } from "react";

import { cn } from "@/lib/utils";

export type PageFiltersProps = Readonly<{
  children: ReactNode;

  className?: string;
}>;

export function PageFilters({
  children,
  className,
}: PageFiltersProps) {
  return (
    <div
      className={cn(
        "flex flex-wrap items-center gap-3",
        className,
      )}
    >
      {children}
    </div>
  );
}
