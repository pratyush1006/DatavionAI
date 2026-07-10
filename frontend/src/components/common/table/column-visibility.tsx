/**
 * Enterprise column visibility menu.
 */

"use client";

import type {
  Table,
} from "@tanstack/react-table";

import {
  Columns3,
} from "lucide-react";

import { Button } from "@/components/ui/button";

import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

export type ColumnVisibilityProps<
  TData,
> = Readonly<{
  table: Table<TData>;
}>;

function formatColumnName(
  value: string,
): string {
  return value
    .replaceAll("_", " ")
    .replace(
      /([a-z])([A-Z])/g,
      "$1 $2",
    )
    .replace(
      /\b\w/g,
      (character) =>
        character.toUpperCase(),
    );
}

export function ColumnVisibility<
  TData,
>({
  table,
}: ColumnVisibilityProps<TData>) {
  const columns = table
    .getAllLeafColumns()
    .filter(
      (column) =>
        column.getCanHide() &&
        column.id !== "actions" &&
        column.id !== "select",
    )
    .sort((left, right) =>
      left.id.localeCompare(right.id),
    );

  return (
    <DropdownMenu>
      <DropdownMenuTrigger
        asChild
      >
        <Button
          variant="outline"
          size="sm"
        >
          <Columns3 className="size-4" />

          Columns
        </Button>
      </DropdownMenuTrigger>

      <DropdownMenuContent
        align="end"
        className="w-56"
      >
        {columns.map((column) => (
          <DropdownMenuCheckboxItem
            key={column.id}
            checked={column.getIsVisible()}
            onCheckedChange={(
              checked,
            ) =>
              column.toggleVisibility(
                checked,
              )
            }
          >
            {formatColumnName(
              column.id,
            )}
          </DropdownMenuCheckboxItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
