/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/organizations/components/tables/organizations-table.tsx
 * =============================================================================
 *
 * Organizations table.
 * =============================================================================
 */

"use client";

import type {
  OrganizationListItem,
} from "../../domain";

import {
  DataTable,
  DataTableLoading,
  EntityTable,
} from "@/components/common/table";

import {
  columns,
} from "./columns";

export type OrganizationsTableProps =
  Readonly<{
    data: OrganizationListItem[];
    isLoading?: boolean;
  }>;

export function OrganizationsTable({
  data,
  isLoading = false,
}: OrganizationsTableProps) {
  return (
    <DataTable>
      {isLoading ? (
        <DataTableLoading />
      ) : (
        <EntityTable
          data={data}
          columns={columns}
          emptyTitle="No organizations found"
          emptyDescription="There are no organizations available."
        />
      )}
    </DataTable>
  );
}
