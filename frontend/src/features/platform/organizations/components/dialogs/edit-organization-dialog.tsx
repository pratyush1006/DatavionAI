/**
 * =============================================================================
 * DatavionOS
 * File:
 * src/features/platform/organizations/components/dialogs/edit-organization-dialog.tsx
 * =============================================================================
 *
 * Edit organization dialog.
 *
 * Responsibilities
 * ----------------
 * - Present the organization edit form.
 * - Load the authoritative organization detail when opened.
 * - Populate the form from the detail response.
 * - Hydrate Geography references for Country -> Region -> City.
 * - Submit only backend-supported mutable fields.
 * - Keep immutable organization fields out of the update payload.
 * - Surface mutation success/error feedback directly below the action button.
 *
 * Architecture
 * ------------
 *
 * OrganizationListItem
 *        |
 *        v
 * EditOrganizationDialog
 *        |
 *        +---- useOrganizationQuery()
 *        |          |
 *        |          v
 *        |    authoritative detail
 *        |
 *        v
 * OrganizationForm
 *        |
 *        v
 * useUpdateOrganizationMutation
 *        |
 *        v
 * Organization API
 *
 * Geography
 * --------
 * countryRef -> regionRef -> cityRef
 *
 * Legacy display fields remain synchronized by AddressInformation:
 *
 * countryRef -> country
 * regionRef  -> state
 * cityRef    -> city
 *
 * Organization code and slug are immutable after creation.
 *
 * Dialog lifecycle
 * ----------------
 * The parent row action owns the dialog open state.
 *
 * This is intentional because the table action lifecycle must remain stable
 * when the Radix dropdown closes.
 * =============================================================================
 */

"use client";

import type {
  Dispatch,
  SetStateAction,
} from "react";

import {
  Pencil,
} from "lucide-react";

import {
  EntityDialog,
} from "@/components/common/dialogs";

import type {
  OrganizationFormValues,
  OrganizationListItem,
} from "../../domain";

import {
  useOrganizationQuery,
  useUpdateOrganizationMutation,
} from "../../hooks";

import {
  OrganizationForm,
} from "../forms";

/* =============================================================================
 * Props
 * =============================================================================
 */

export type EditOrganizationDialogProps =
  Readonly<{
    /**
     * The list representation supplied by the organization table.
     *
     * The full organization detail is fetched when the dialog opens.
     */
    organization:
      OrganizationListItem;

    /**
     * Controlled dialog state.
     *
     * The parent row action owns this state so the dialog survives the
     * dropdown-menu lifecycle.
     */
    open:
      boolean;

    /**
     * Controlled dialog state setter.
     */
    onOpenChange:
      Dispatch<SetStateAction<boolean>>;
  }>;

/* =============================================================================
 * Component
 * =============================================================================
 */

export function EditOrganizationDialog({
  organization,
  open,
  onOpenChange,
}: EditOrganizationDialogProps) {
  const mutation =
    useUpdateOrganizationMutation();

  /**
   * Fetch authoritative organization detail only when the dialog is open.
   */
  const detailQuery =
    useOrganizationQuery(
      organization.id,
      open,
    );

  /* ===========================================================================
   * Submit
   * =========================================================================== */

  async function handleSubmit(
    values: OrganizationFormValues,
  ): Promise<void> {
    /**
     * Clear previous mutation feedback before starting a new request.
     *
     * OrganizationForm owns the presentation of this feedback, while the
     * mutation itself remains responsible for the API operation.
     */
    try {
      /**
       * Code and slug are immutable after creation.
       *
       * Build the update payload explicitly so immutable fields can never
       * accidentally reach the update API.
       *
       * Geography references are submitted together with the legacy
       * human-readable address fields.
       */
      const payload = {
        name:
          values.name,

        displayName:
          values.displayName,

        category:
          values.category,

        organizationType:
          values.organizationType,

        size:
          values.size,

        status:
          values.status,

        email:
          values.email,

        supportEmail:
          values.supportEmail,

        phone:
          values.phone,

        website:
          values.website,

        address:
          values.address,

        /**
         * Legacy compatibility fields.
         *
         * AddressInformation keeps these synchronized with the selected
         * Geography records.
         */
        city:
          values.city,

        state:
          values.state,

        country:
          values.country,

        /**
         * Canonical Geography references.
         */
        countryRef:
          values.countryRef,

        regionRef:
          values.regionRef,

        cityRef:
          values.cityRef,

        postalCode:
          values.postalCode,

        timezone:
          values.timezone,

        registrationNumber:
          values.registrationNumber,

        taxNumber:
          values.taxNumber,

        licenseNumber:
          values.licenseNumber,

        accreditation:
          values.accreditation,

        description:
          values.description,

        isDemo:
          values.isDemo,
      };

      await mutation.mutateAsync({
        id:
          organization.id,

        payload,
      });

      /**
       * Do not close the dialog here.
       *
       * The success message is intentionally rendered by OrganizationForm
       * directly below the action button so the user receives contextual
       * confirmation of the completed operation.
       */
    } catch {
      /**
       * The mutation error is surfaced through mutation.error and passed to
       * OrganizationForm below.
       *
       * Keeping the error in the mutation state also means retrying the
       * operation naturally replaces the previous error with the next result.
       */
    }
  }

  /* ===========================================================================
   * Mutation feedback
   * =============================================================================
   */

  const mutationError =
    mutation.error instanceof Error
      ? mutation.error.message
      : mutation.error
        ? "Unable to update organization."
        : null;

  const successMessage =
    mutation.isSuccess
      ? "Organization updated successfully."
      : null;

  /* ===========================================================================
   * Render
   * =============================================================================
   */

  return (
    <>
      <button
        type="button"
        className="inline-flex h-8 w-8 items-center justify-center rounded-md text-sm font-medium transition-colors hover:bg-muted hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50"
        onClick={() =>
          onOpenChange(true)
        }
        disabled={
          mutation.isPending
        }
        aria-label="Edit organization"
      >
        <Pencil className="h-4 w-4" />

        <span className="sr-only">
          Edit organization
        </span>
      </button>

      <EntityDialog
        open={open}
        onOpenChange={onOpenChange}
        title="Edit Organization"
        description="Update organization information."
        size="xl"
      >
        {detailQuery.isPending ? (
          <p className="py-8 text-sm text-muted-foreground">
            Loading organization details...
          </p>
        ) : detailQuery.isError ? (
          <p
            role="alert"
            className="py-8 text-sm text-destructive"
          >
            {detailQuery.error instanceof Error
              ? detailQuery.error.message
              : "Unable to load organization details."}
          </p>
        ) : detailQuery.data ? (
          <OrganizationForm
            defaultValues={{
              /* -----------------------------------------------------------------
               * General
               * ----------------------------------------------------------------- */

              name:
                detailQuery.data.name,

              displayName:
                detailQuery.data.displayName,

              /**
               * These are displayed/read-only by the GeneralInformation
               * section but are retained for form hydration.
               */
              code:
                detailQuery.data.code,

              slug:
                detailQuery.data.slug,

              category:
                detailQuery.data.category,

              organizationType:
                detailQuery.data.organizationType,

              size:
                detailQuery.data.size,

              status:
                detailQuery.data.status,

              /* -----------------------------------------------------------------
               * Contact
               * ----------------------------------------------------------------- */

              email:
                detailQuery.data.email,

              supportEmail:
                detailQuery.data.supportEmail,

              phone:
                detailQuery.data.phone,

              website:
                detailQuery.data.website,

              /* -----------------------------------------------------------------
               * Address
               * ----------------------------------------------------------------- */

              address:
                detailQuery.data.address,

              /**
               * Legacy display fields.
               */
              city:
                detailQuery.data.city,

              state:
                detailQuery.data.state,

              country:
                detailQuery.data.country,

              /**
               * Canonical Geography references.
               *
               * These values hydrate the Country -> Region -> City dropdowns.
               */
              countryRef:
                detailQuery.data.countryRef,

              regionRef:
                detailQuery.data.regionRef,

              cityRef:
                detailQuery.data.cityRef,

              postalCode:
                detailQuery.data.postalCode,

              timezone:
                detailQuery.data.timezone,

              /* -----------------------------------------------------------------
               * Legal
               * ----------------------------------------------------------------- */

              registrationNumber:
                detailQuery.data.registrationNumber,

              taxNumber:
                detailQuery.data.taxNumber,

              licenseNumber:
                detailQuery.data.licenseNumber,

              accreditation:
                detailQuery.data.accreditation,

              description:
                detailQuery.data.description,

              isDemo:
                detailQuery.data.isDemo,
            }}
            isSubmitting={
              mutation.isPending
            }
            isEdit
            successMessage={
              successMessage
            }
            errorMessage={
              mutationError
            }
            onSubmit={
              handleSubmit
            }
            onCancel={() =>
              onOpenChange(false)
            }
          />
        ) : null}
      </EntityDialog>
    </>
  );
}
