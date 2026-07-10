/**
 * Delete organization dialog.
 */

"use client";

import { useState } from "react";

import { AxiosError } from "axios";
import { Trash2 } from "lucide-react";
import { toast } from "sonner";

import {
  ConfirmDialog,
} from "@/components/common/dialogs";

import { Button } from "@/components/ui/button";

import type {
  Organization,
} from "../../domain";

import {
  useDeleteOrganizationMutation,
} from "../../hooks";

type ApiError = {
  error?: {
    message?: string;
  };
};

export type DeleteOrganizationDialogProps =
  Readonly<{
    organization: Organization;
  }>;

export function DeleteOrganizationDialog({
  organization,
}: DeleteOrganizationDialogProps) {
  const [open, setOpen] =
    useState(false);

  const mutation =
    useDeleteOrganizationMutation();

  async function handleDelete() {
    try {
      await mutation.mutateAsync(
        organization.id,
      );

      toast.success(
        "Organization deleted successfully.",
      );

      setOpen(false);
    } catch (error) {
      const axiosError =
        error as AxiosError<ApiError>;

      const message =
        axiosError.response?.data?.error
          ?.message ??
        "Unable to delete organization.";

      toast.error(message);
    }
  }

  return (
    <>
      <Button
        variant="ghost"
        size="icon-sm"
        onClick={() =>
          setOpen(true)
        }
      >
        <Trash2 className="h-4 w-4" />

        <span className="sr-only">
          Delete organization
        </span>
      </Button>

      <ConfirmDialog
        open={open}
        onOpenChange={setOpen}
        title="Delete Organization"
        description={
          <>
            Are you sure you want to delete{" "}
            <strong>
              {organization.name}
            </strong>
            ? This action cannot be
            undone.
          </>
        }
        confirmLabel="Delete"
        confirmVariant="destructive"
        isLoading={
          mutation.isPending
        }
        onConfirm={
          handleDelete
        }
      />
    </>
  );
}
