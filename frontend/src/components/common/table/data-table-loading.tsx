/**
 * Enterprise data table loading state.
 */

"use client";

import { Skeleton } from "@/components/ui/skeleton";

import { cn } from "@/lib/utils";

export type DataTableLoadingProps = Readonly<{
  rows?: number;

  columns?: number;

  className?: string;
}>;

export function DataTableLoading({
  rows = 10,
  columns = 6,
  className,
}: DataTableLoadingProps) {
  return (
    <div
      className={cn(
        "rounded-lg border border-border",
        className,
      )}
    >
      <div className="border-b bg-muted/40 p-4">
        <Skeleton className="h-5 w-48" />
      </div>

      <div className="divide-y">
        {Array.from({
          length: rows,
        }).map((_, rowIndex) => (
          <div
            key={rowIndex}
            className="grid gap-4 p-4"
            style={{
              gridTemplateColumns: `repeat(${columns}, minmax(0, 1fr))`,
            }}
          >
            {Array.from({
              length: columns,
            }).map((__, columnIndex) => (
              <Skeleton
                key={columnIndex}
                className="h-5 w-full"
              />
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}
