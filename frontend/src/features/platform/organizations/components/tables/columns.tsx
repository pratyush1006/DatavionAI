/**
 * Organization table columns.
 */

"use client";

import type { ColumnDef } from "@tanstack/react-table";
import { Building2 } from "lucide-react";

import {
  RowActions,
} from "@/components/common/table";

import { Badge } from "@/components/ui/badge";

import type {
  Organization,
} from "../../domain";

export const columns: ColumnDef<Organization>[] = [
  {
    accessorKey: "name",

    header: "Organization",

    cell: ({ row }) => {
      const organization = row.original;

      return (
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
            <Building2 className="h-5 w-5 text-primary" />
          </div>

          <div>
            <div className="font-medium">
              {organization.name}
            </div>

            <div className="text-xs text-muted-foreground">
              {organization.code}
            </div>
          </div>
        </div>
      );
    },
  },

  {
    accessorKey: "organizationType",

    header: "Type",

    cell: ({ row }) => (
      <Badge variant="secondary">
        {row.original.organizationType.replaceAll(
          "_",
          " ",
        )}
      </Badge>
    ),
  },

  {
    accessorKey: "email",

    header: "Contact",

    cell: ({ row }) => (
      <div>
        <div>{row.original.email}</div>

        <div className="text-xs text-muted-foreground">
          {row.original.phone}
        </div>
      </div>
    ),
  },

  {
    id: "location",

    header: "Location",

    cell: ({ row }) => (
      <div>
        <div>{row.original.city}</div>

        <div className="text-xs text-muted-foreground">
          {row.original.state},{" "}
          {row.original.country}
        </div>
      </div>
    ),
  },

  {
    accessorKey: "isActive",

    header: "Status",

    cell: ({ row }) => (
      <Badge
        variant={
          row.original.isActive
            ? "default"
            : "destructive"
        }
      >
        {row.original.isActive
          ? "Active"
          : "Inactive"}
      </Badge>
    ),
  },

  {
    id: "actions",

    header: "",

    enableSorting: false,

    enableHiding: false,

    cell: () => (
      <RowActions>
        <div className="p-2 text-sm">
          Test Menu
        </div>
      </RowActions>
    ),
  },
];
