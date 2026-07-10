/**
 * Enterprise entity table.
 */

"use client";

import type {
  ColumnDef,
  Table as TanStackTable,
} from "@tanstack/react-table";

import {
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";

import {
  DataTableEmpty,
} from "./data-table-empty";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

import { cn } from "@/lib/utils";

export type EntityTableProps<TData> = Readonly<{
  data: readonly TData[];

  columns: readonly ColumnDef<TData>[];

  className?: string;

  emptyTitle?: string;

  emptyDescription?: string;

  onTableReady?: (
    table: TanStackTable<TData>,
  ) => void;
}>;

export function EntityTable<TData>({
  data,
  columns,
  className,
  emptyTitle,
  emptyDescription,
  onTableReady,
}: EntityTableProps<TData>) {
  const table = useReactTable({
    data: [...data],
    columns: [...columns],
    getCoreRowModel:
      getCoreRowModel(),
  });

  onTableReady?.(table);

  return (
    <div
      className={cn(
        "overflow-hidden rounded-xl border bg-card",
        className,
      )}
    >
      <Table>
        <TableHeader>
          {table
            .getHeaderGroups()
            .map((headerGroup) => (
              <TableRow
                key={headerGroup.id}
              >
                {headerGroup.headers.map(
                  (header) => (
                    <TableHead
                      key={header.id}
                    >
                      {header.isPlaceholder
                        ? null
                        : flexRender(
                            header.column
                              .columnDef.header,
                            header.getContext(),
                          )}
                    </TableHead>
                  ),
                )}
              </TableRow>
            ))}
        </TableHeader>

        <TableBody>
          {table
            .getRowModel()
            .rows.length > 0 ? (
            table
              .getRowModel()
              .rows.map((row) => (
                <TableRow
                  key={row.id}
                  data-state={
                    row.getIsSelected()
                      ? "selected"
                      : undefined
                  }
                >
                  {row
                    .getVisibleCells()
                    .map((cell) => (
                      <TableCell
                        key={cell.id}
                      >
                        {flexRender(
                          cell.column
                            .columnDef.cell,
                          cell.getContext(),
                        )}
                      </TableCell>
                    ))}
                </TableRow>
              ))
          ) : (
            <TableRow>
              <TableCell
                colSpan={
                  columns.length
                }
                className="p-0"
              >
                <DataTableEmpty
                  title={
                    emptyTitle
                  }
                  description={
                    emptyDescription
                  }
                />
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </div>
  );
}
