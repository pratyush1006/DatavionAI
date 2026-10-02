/**
 * Enterprise reusable data table wrapper.
 */

"use client";

import type { ReactNode } from "react";

import { cn } from "@/lib/utils";

export type DataTableProps = Readonly<{
  toolbar?: ReactNode;

  children: ReactNode;

  pagination?: ReactNode;

  className?: string;
}>;

export function DataTable({
  toolbar,
  children,
  pagination,
  className,
}: DataTableProps) {
  return (
    <section
      className={cn(
        "space-y-4",
        className,
      )}
    >
      {toolbar}

      <div className="space-y-4">
        {children}
      </div>

      {pagination}
    </section>
  );
}
