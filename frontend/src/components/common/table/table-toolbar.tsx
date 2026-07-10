/**
 * Enterprise table toolbar.
 *
 * Displays selection state and contextual actions
 * for an entity table.
 */

"use client";

import type { ReactNode } from "react";

import { RefreshCw } from "lucide-react";

import { Button } from "@/components/ui/button";

import { cn } from "@/lib/utils";

export type TableToolbarProps = Readonly<{
  /**
   * Number of selected rows.
   */
  selectedCount?: number;

  /**
   * Refresh callback.
   */
  onRefresh?: () => void;

  /**
   * Actions displayed on the right.
   * Example:
   * - Column visibility
   * - Export
   * - Density
   */
  actions?: ReactNode;

  /**
   * Bulk actions displayed when rows are selected.
   */
  bulkActions?: ReactNode;

  className?: string;
}>;

export function TableToolbar({
  selectedCount = 0,
  onRefresh,
  actions,
  bulkActions,
  className,
}: TableToolbarProps) {
  const hasSelection = selectedCount > 0;

  return (
    <div
      className={cn(
        "flex flex-col gap-3 border-b bg-muted/30 px-4 py-3",
        "lg:flex-row lg:items-center lg:justify-between",
        className,
      )}
    >
      <div className="flex items-center gap-3">
        {hasSelection ? (
          <>
            <span className="text-sm font-medium">
              {selectedCount} selected
            </span>

            {bulkActions}
          </>
        ) : (
          <span className="text-sm text-muted-foreground">
            No items selected
          </span>
        )}
      </div>

      <div className="flex flex-wrap items-center gap-2">
        {actions}

        {onRefresh && (
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={onRefresh}
          >
            <RefreshCw className="size-4" />

            Refresh
          </Button>
        )}
      </div>
    </div>
  );
}
