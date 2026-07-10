/**
 * Enterprise page pagination.
 */

"use client";

import {
  ChevronLeft,
  ChevronRight,
} from "lucide-react";

import { Button } from "@/components/ui/button";

import { cn } from "@/lib/utils";

export type PagePaginationProps = Readonly<{
  page: number;

  totalPages: number;

  onPageChange: (
    page: number,
  ) => void;

  className?: string;
}>;

export function PagePagination({
  page,
  totalPages,
  onPageChange,
  className,
}: PagePaginationProps) {
  const canGoPrevious = page > 1;

  const canGoNext = page < totalPages;

  return (
    <div
      className={cn(
        "flex flex-col gap-4 border-t pt-4",
        "sm:flex-row sm:items-center sm:justify-between",
        className,
      )}
    >
      <p className="text-sm text-muted-foreground">
        Page{" "}
        <span className="font-medium">
          {page}
        </span>{" "}
        of{" "}
        <span className="font-medium">
          {totalPages}
        </span>
      </p>

      <div className="flex items-center gap-2">
        <Button
          type="button"
          variant="outline"
          size="sm"
          disabled={!canGoPrevious}
          onClick={() =>
            onPageChange(page - 1)
          }
        >
          <ChevronLeft className="mr-2 h-4 w-4" />

          Previous
        </Button>

        <Button
          type="button"
          variant="outline"
          size="sm"
          disabled={!canGoNext}
          onClick={() =>
            onPageChange(page + 1)
          }
        >
          Next

          <ChevronRight className="ml-2 h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}
