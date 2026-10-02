/**
 * =============================================================================
 * DatavionOS
 * File:
 * src/features/platform/organizations/components/dialogs/create-organization-dialog.tsx
 * =============================================================================
 *
 * Create organization dialog.
 *
 * Responsibilities
 * ----------------
 * - Open and close the create organization dialog.
 * - Submit organization creation requests.
 * - Surface success/error feedback directly below the form action.
 * - Avoid global toast notifications for contextual mutation results.
 * =============================================================================
 */

"use client";

import {
  useState,
} from "react";

import {
  Plus,
} from "lucide-react";

import {
  EntityDialog,
} from "@/components/common/dialogs";

import {
  Button,
} from "@/components/ui/button";

import type {
  OrganizationFormValues,
} from "../../domain";

import {
  useCreateOrganizationMutation,
} from "../../hooks";

import {
  OrganizationForm,
} from "../forms";

/* =============================================================================
 * Component
 * =============================================================================
 */

export function CreateOrganizationDialog() {
  const [
    open,
    setOpen,
  ] = useState(false);

  const [
    successMessage,
    setSuccessMessage,
  ] = useState<
    string | null
  >(null);

  const [
    errorMessage,
    setErrorMessage,
  ] = useState<
    string | null
  >(null);

  const mutation =
    useCreateOrganizationMutation();

  /* ===========================================================================
   * Dialog lifecycle
   * =========================================================================== */

  function handleOpenChange(
    nextOpen: boolean,
  ): void {
    setOpen(nextOpen);

    if (!nextOpen) {
      setSuccessMessage(null);
      setErrorMessage(null);
    }
  }

  function handleOpen(): void {
    setSuccessMessage(null);
    setErrorMessage(null);
    setOpen(true);
  }

  /* ===========================================================================
   * Submit
   * =========================================================================== */

  async function handleSubmit(
    values: OrganizationFormValues,
  ): Promise<void> {
    setSuccessMessage(null);
    setErrorMessage(null);

    try {
      await mutation.mutateAsync(
        values,
      );

      setSuccessMessage(
        "Organization created successfully.",
      );
    } catch (error) {
      const message =
        error instanceof Error
          ? error.message
          : "Unable to create organization.";

      setErrorMessage(message);
    }
  }

  /* ===========================================================================
   * Render
   * =========================================================================== */

  return (
    <>
      <Button
        type="button"
        onClick={
          handleOpen
        }
        disabled={
          mutation.isPending
        }
      >
        <Plus className="mr-2 h-4 w-4" />

        New Organization
      </Button>

      <EntityDialog
        open={open}
        onOpenChange={
          handleOpenChange
        }
        title="Create Organization"
        description="Create a new organization in the Datavion AI platform."
        size="xl"
      >
        <OrganizationForm
          isSubmitting={
            mutation.isPending
          }
          successMessage={
            successMessage
          }
          errorMessage={
            errorMessage
          }
          onSubmit={
            handleSubmit
          }
          onCancel={() =>
            handleOpenChange(false)
          }
        />
      </EntityDialog>
    </>
  );
}
