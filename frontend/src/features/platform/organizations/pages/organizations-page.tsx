/**
 * Organizations page.
 */

"use client";

import { ListPage } from "@/components/common/page";

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

import { CreateOrganizationDialog } from "../components/dialogs";
import { OrganizationsTable } from "../components/tables";
import { useOrganizationsQuery } from "../hooks";

export function OrganizationsPage() {
  const {
    data = [],
    isPending,
  } = useOrganizationsQuery();

  return (
    <ListPage
      title="Organizations"
      description="Manage organizations across the Datavion AI platform."
      actions={<CreateOrganizationDialog />}
    >
      <div className="mb-6">
        <DropdownMenu>
          <DropdownMenuTrigger className="rounded border px-4 py-2">
            Open Menu
          </DropdownMenuTrigger>

          <DropdownMenuContent>
            <DropdownMenuItem>
              Test Item
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>

      <OrganizationsTable
        data={data}
        isLoading={isPending}
      />
    </ListPage>
  );
}
