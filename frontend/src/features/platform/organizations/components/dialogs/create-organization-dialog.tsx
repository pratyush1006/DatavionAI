/**
 * Create organization dialog.
 */

"use client";

import { useState } from "react";

import { AxiosError } from "axios";
import { Plus } from "lucide-react";
import { toast } from "sonner";

import { EntityDialog } from "@/components/common/dialogs";
import { Button } from "@/components/ui/button";

import type {
  OrganizationFormValues,
} from "../../domain";

import {
  useCreateOrganizationMutation,
} from "../../hooks";

import {
  OrganizationForm,
} from "../forms";

type ApiError = {
  error?: {
    message?: string;
  };
};

export function CreateOrganizationDialog() {
  const [open, setOpen] =
    useState(false);

  const mutation =
    useCreateOrganizationMutation();

  async function handleSubmit(
    values: OrganizationFormValues,
  ) {
    try {
      await mutation.mutateAsync(values);

      toast.success(
        "Organization created successfully.",
      );

      setOpen(false);
    } catch (error) {
      const axiosError =
        error as AxiosError<ApiError>;

      const message =
        axiosError.response?.data?.error
          ?.message ??
        "Unable to create organization.";

      toast.error(message);
    }
  }

  return (
    <>
      <Button
        onClick={() =>
          setOpen(true)
        }
      >
        <Plus className="mr-2 h-4 w-4" />

        New Organization
      </Button>

      <EntityDialog
        open={open}
        onOpenChange={setOpen}
        title="Create Organization"
        description="Create a new organization in the Datavion AI platform."
        size="xl"
      >
        <OrganizationForm
          isSubmitting={
            mutation.isPending
          }
          onSubmit={
            handleSubmit
          }
          onCancel={() =>
            setOpen(false)
          }
        />
      </EntityDialog>
    </>
  );
}
