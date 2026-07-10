/**
 * Responsive form grid.
 */

import type { ReactNode } from "react";

import { cn } from "@/lib/utils";

export type FormGridProps =
  Readonly<{
    children: ReactNode;

    columns?: 1 | 2 | 3;

    className?: string;
  }>;

const GRID_COLUMNS = {
  1: "grid-cols-1",
  2: "grid-cols-1 lg:grid-cols-2",
  3: "grid-cols-1 md:grid-cols-2 xl:grid-cols-3",
} as const;

export function FormGrid({
  children,
  columns = 2,
  className,
}: FormGridProps) {
  return (
    <div
      className={cn(
        "grid gap-6",
        GRID_COLUMNS[columns],
        className,
      )}
    >
      {children}
    </div>
  );
}
