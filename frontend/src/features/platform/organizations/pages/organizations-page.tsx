/**
 * Organizations page.
 */

"use client";

import { ListPage } from "@/components/common/page";
import { EmptyState } from "@/components/common/page";
import { Button } from "@/components/ui/button";

import { CreateOrganizationDialog } from "../components/dialogs";
import { OrganizationsTable } from "../components/tables";
import { useOrganizationsQuery } from "../hooks";

export function OrganizationsPage() {
  const {
    data = [],
    isPending,
    isError,
    error,
    refetch,
  } = useOrganizationsQuery();

  return (
    <ListPage
      title="Organizations"
      description="Manage organizations across the Datavion AI platform."
      actions={<CreateOrganizationDialog />}
    >
      {isError ? (
        <EmptyState
          title="Could not load organizations"
          description={
            error instanceof Error
              ? error.message
              : "Please check your connection and try again."
          }
          action={
            <Button onClick={() => void refetch()}>
              Try again
            </Button>
          }
        />
      ) : (
        <OrganizationsTable
          data={data}
          isLoading={isPending}
        />
      )}
    </ListPage>
  );
}
