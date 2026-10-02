/*
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/organizations/components/tables/columns.tsx
 * =============================================================================
 *
 * Organization table columns.
 *
 * Action dialogs are deliberately rendered outside the dropdown menu lifecycle.
 * =============================================================================
 */

"use client";

import {
  useState,
} from "react";

import type {
  ColumnDef,
} from "@tanstack/react-table";

import {
  Archive,
  Building2,
} from "lucide-react";

import {
  RowActions,
} from "@/components/common/table";

import {
  Badge,
} from "@/components/ui/badge";

import {
  DropdownMenuItem,
} from "@/components/ui/dropdown-menu";

import type {
  OrganizationListItem,
} from "../../domain";

import {
  DeleteOrganizationDialog,
  EditOrganizationDialog,
} from "../dialogs";

/* =============================================================================
 * Organization Row Actions
 * =============================================================================
 *
 * The dropdown contains action menu items only.
 *
 * Dialogs are rendered outside RowActions so closing the Radix dropdown does
 * not unmount the dialog that was just requested.
 * =============================================================================
 */

type OrganizationRowActionsProps =
  Readonly<{
    organization: OrganizationListItem;
  }>;

function OrganizationRowActions({
  organization,
}: OrganizationRowActionsProps) {
  const [
    editOpen,
    setEditOpen,
  ] = useState(false);

  const [
    archiveOpen,
    setArchiveOpen,
  ] = useState(false);

  return (
    <div className="flex items-center justify-end">
      <RowActions>
        <DropdownMenuItem
          onSelect={(event) => {
            event.preventDefault();
            setEditOpen(true);
          }}
        >
          <span>
            Edit organization
          </span>
        </DropdownMenuItem>

        <DropdownMenuItem
          variant="destructive"
          onSelect={(event) => {
            event.preventDefault();
            setArchiveOpen(true);
          }}
        >
          <Archive className="size-4" />

          <span>
            Archive organization
          </span>
        </DropdownMenuItem>
      </RowActions>

      <EditOrganizationDialog
        organization={
          organization
        }
        open={
          editOpen
        }
        onOpenChange={
          setEditOpen
        }
      />

      <DeleteOrganizationDialog
        organization={
          organization
        }
        open={
          archiveOpen
        }
        onOpenChange={
          setArchiveOpen
        }
      />
    </div>
  );
}

/* =============================================================================
 * Columns
 * =============================================================================
 */

export const columns:
  ColumnDef<OrganizationListItem>[] = [
    {
      accessorKey: "displayName",

      header: "Organization",

      cell: ({ row }) => {
        const organization =
          row.original;

        return (
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
              <Building2 className="h-5 w-5 text-primary" />
            </div>

            <div>
              <div className="font-medium">
                {organization.displayName || "-"}
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
          {row.original.organizationType
            ? row.original.organizationType.replaceAll(
                "_",
                " ",
              )
            : "-"}
        </Badge>
      ),
    },

    {
      accessorKey: "category",

      header: "Category",

      cell: ({ row }) =>
        row.original.category || "-",
    },

    {
      accessorKey: "status",

      header: "Status",

      cell: ({ row }) => (
        <Badge variant="secondary">
          {row.original.status || "-"}
        </Badge>
      ),
    },

    {
      id: "location",

      header: "Location",

      cell: ({ row }) => (
        <div>
          <div>
            {row.original.city || "-"}
          </div>

          <div className="text-xs text-muted-foreground">
            {row.original.country || "-"}
          </div>
        </div>
      ),
    },

    {
      id: "actions",

      header: "",

      enableSorting: false,

      enableHiding: false,

      cell: ({ row }) => (
        <OrganizationRowActions
          organization={
            row.original
          }
        />
      ),
    },
  ];
