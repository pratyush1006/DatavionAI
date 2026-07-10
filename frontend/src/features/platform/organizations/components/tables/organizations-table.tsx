/**
 * Organizations table.
 */

"use client";

import type {
  Organization,
} from "../../domain";

import {
  DataTable,
  EntityTable,
} from "@/components/common/table";

import { columns } from "./columns";

export type OrganizationsTableProps =
  Readonly<{
    data: Organization[];
    isLoading?: boolean;
  }>;

export function OrganizationsTable({
  data,
  isLoading = false,
}: OrganizationsTableProps) {
  return (
    <DataTable
      loading={isLoading}
    >
      <EntityTable
        data={data}
        columns={columns}
      />
    </DataTable>
  );
}
