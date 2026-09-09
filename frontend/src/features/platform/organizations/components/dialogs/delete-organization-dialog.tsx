/**
 * =============================================================================
 * DatavionOS
 * File:
 * src/features/platform/organizations/components/dialogs/delete-organization-dialog.tsx
 * =============================================================================
 *
 * Organization archive dialog.
 *
 * Organization deletion is implemented as a soft archive. The record remains
 * retained by the platform and is removed from the normal active collection.
 *
 * The dialog is controlled by the parent row action so that it remains outside
 * the Radix dropdown lifecycle.
 *
 * Contextual mutation feedback is rendered directly below the Archive button.
 * =============================================================================
 */

"use client";

import {
  ConfirmDialog,
} from "@/components/common/dialogs";

import type {
  OrganizationListItem,
} from "../../domain";

import {
  useDeleteOrganizationMutation,
} from "../../hooks";

/* =============================================================================
 * Props
 * =============================================================================
 */

export type DeleteOrganizationDialogProps =
  Readonly<{
    organization:
      OrganizationListItem;

    open:
      boolean;

    onOpenChange:
      (open: boolean) => void;
  }>;

/* =============================================================================
 * Component
 * =============================================================================
 */

export function DeleteOrganizationDialog({
  organization,
  open,
  onOpenChange,
}: DeleteOrganizationDialogProps) {
  const mutation =
    useDeleteOrganizationMutation();

  /* ===========================================================================
   * Archive
   * =========================================================================== */

  async function handleDelete(): Promise<void> {
    try {
      await mutation.mutateAsync(
        organization.id,
      );
    } catch {
      /**
       * The mutation error is exposed through mutation.error and rendered by
       * ConfirmDialog below.
       *
       * We intentionally do not close the dialog on failure so the user can
       * see the contextual error and retry.
       */
    }
  }

  /* ===========================================================================
   * Mutation feedback
   * =========================================================================== */

  const successMessage =
    mutation.isSuccess
      ? "Organization archived successfully."
      : null;

  const errorMessage =
    mutation.error instanceof Error
      ? mutation.error.message
      : mutation.error
        ? "Unable to archive organization."
        : null;

  /* ===========================================================================
   * Render
   * =========================================================================== */

  return (
    <ConfirmDialog
      open={open}
      onOpenChange={onOpenChange}
      title="Archive Organization"
      description={
        <>
          Are you sure you want to archive{" "}
          <strong>
            {
              organization.displayName ||
              organization.code
            }
          </strong>
          ? Archived organizations are retained by the platform.
        </>
      }
      confirmLabel="Archive"
      cancelLabel="Cancel"
      confirmVariant="destructive"
      isLoading={
        mutation.isPending
      }
      successMessage={
        successMessage
      }
      errorMessage={
        errorMessage
      }
      onConfirm={
        handleDelete
      }
    />
  );
}
