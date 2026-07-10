/**
 * Enterprise data table pagination.
 */

"use client";

import { ChevronLeft, ChevronRight } from "lucide-react";

import { Button } from "@/components/ui/button";

import { cn } from "@/lib/utils";

export type DataTablePaginationProps = Readonly<{
  page: number;

  pageSize: number;

  totalItems: number;

  onPageChange: (
    page: number,
  ) => void;

  className?: string;
}>;

export function DataTablePagination({
  page,
  pageSize,
  totalItems,
  onPageChange,
  className,
}: DataTablePaginationProps) {
  const totalPages = Math.max(
    1,
    Math.ceil(totalItems / pageSize),
  );

  const start =
    totalItems === 0
      ? 0
      : (page - 1) * pageSize + 1;

  const end = Math.min(
    page * pageSize,
    totalItems,
  );

  return (
    <div
      className={cn(
        "flex flex-col gap-4 border-t pt-4 sm:flex-row sm:items-center sm:justify-between",
        className,
      )}
    >
      <p className="text-sm text-muted-foreground">
        Showing{" "}
        <span className="font-medium">
          {start}
        </span>{" "}
        to{" "}
        <span className="font-medium">
          {end}
        </span>{" "}
        of{" "}
        <span className="font-medium">
          {totalItems}
        </span>{" "}
        entries
      </p>

      <div className="flex items-center gap-2">
        <Button
          type="button"
          variant="outline"
          size="sm"
          disabled={page <= 1}
          onClick={() =>
            onPageChange(page - 1)
          }
        >
          <ChevronLeft className="size-4" />
          Previous
        </Button>

        <span className="min-w-20 text-center text-sm">
          {page} / {totalPages}
        </span>

        <Button
          type="button"
          variant="outline"
          size="sm"
          disabled={
            page >= totalPages
          }
          onClick={() =>
            onPageChange(page + 1)
          }
        >
          Next
          <ChevronRight className="size-4" />
        </Button>
      </div>
    </div>
  );
}
