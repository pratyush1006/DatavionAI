/**
 * Edit organization dialog.
 */

"use client";

import { useState } from "react";

import { AxiosError } from "axios";
import { Pencil } from "lucide-react";
import { toast } from "sonner";

import { EntityDialog } from "@/components/common/dialogs";
import { Button } from "@/components/ui/button";

import type {
  Organization,
  OrganizationFormValues,
} from "../../domain";

import {
  useUpdateOrganizationMutation,
} from "../../hooks";

import {
  OrganizationForm,
} from "../forms";

type ApiError = {
  error?: {
    message?: string;
  };
};

export type EditOrganizationDialogProps =
  Readonly<{
    organization: Organization;
  }>;

export function EditOrganizationDialog({
  organization,
}: EditOrganizationDialogProps) {
  const [open, setOpen] =
    useState(false);

  const mutation =
    useUpdateOrganizationMutation();

  async function handleSubmit(
    values: OrganizationFormValues,
  ) {
    try {
      await mutation.mutateAsync({
        id: organization.id,
        payload: values,
      });

      toast.success(
        "Organization updated successfully.",
      );

      setOpen(false);
    } catch (error) {
      const axiosError =
        error as AxiosError<ApiError>;

      const message =
        axiosError.response?.data?.error
          ?.message ??
        "Unable to update organization.";

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
        <Pencil className="h-4 w-4" />

        <span className="sr-only">
          Edit organization
        </span>
      </Button>

      <EntityDialog
        open={open}
        onOpenChange={setOpen}
        title="Edit Organization"
        description="Update organization information."
        size="xl"
      >
        <OrganizationForm
          defaultValues={{
            name: organization.name,
            code: organization.code,
            organizationType:
              organization.organizationType,
            email: organization.email,
            phone: organization.phone,
            address: organization.address,
            city: organization.city,
            state: organization.state,
            country: organization.country,
            isActive:
              organization.isActive,
          }}
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
