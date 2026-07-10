/**
 * Enterprise data table filters container.
 */

"use client";

import type {
  ReactNode,
} from "react";

import { cn } from "@/lib/utils";

export type DataTableFiltersProps = Readonly<{
  children: ReactNode;

  className?: string;
}>;

export function DataTableFilters({
  children,
  className,
}: DataTableFiltersProps) {
  return (
    <div
      className={cn(
        "flex flex-wrap items-center gap-2",
        className,
      )}
    >
      {children}
    </div>
  );
}
