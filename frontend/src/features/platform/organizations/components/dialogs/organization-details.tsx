/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/organizations/components/dialogs/organization-details.tsx
 * =============================================================================
 *
 * Organization details dialog.
 *
 * Displays backend-authoritative organization information using the frontend
 * Organization domain model.
 * =============================================================================
 */

"use client";

import type {
  ReactNode,
} from "react";

import {
  Building2,
  Globe,
  Mail,
  MapPin,
  Phone,
} from "lucide-react";

import {
  EntityDialog,
} from "@/components/common/dialogs";

import {
  Badge,
} from "@/components/ui/badge";

import type {
  Organization,
} from "../../domain";

/* =============================================================================
 * Props
 * =============================================================================
 */

export type OrganizationDetailsProps =
  Readonly<{
    organization: Organization;

    open: boolean;

    onOpenChange: (
      open: boolean,
    ) => void;
  }>;

/* =============================================================================
 * Component
 * =============================================================================
 */

export function OrganizationDetails({
  organization,
  open,
  onOpenChange,
}: OrganizationDetailsProps) {
  return (
    <EntityDialog
      open={open}
      onOpenChange={onOpenChange}
      title={
        organization.displayName ||
        organization.name
      }
      description="Organization details"
      size="xl"
    >
      <div className="space-y-6">
        {/* =====================================================================
         * Header
         * ===================================================================== */}

        <div className="flex items-start gap-4">
          <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-lg bg-primary/10">
            <Building2 className="h-6 w-6 text-primary" />
          </div>

          <div className="min-w-0 flex-1">
            <h3 className="text-lg font-semibold">
              {organization.name}
            </h3>

            <p className="text-sm text-muted-foreground">
              {organization.code}
            </p>

            <div className="mt-2 flex flex-wrap gap-2">
              <Badge variant="secondary">
                {organization.organizationType
                  ? organization.organizationType.replaceAll(
                      "_",
                      " ",
                    )
                  : "-"}
              </Badge>

              {organization.category && (
                <Badge variant="outline">
                  {organization.category}
                </Badge>
              )}

              {organization.status && (
                <Badge variant="secondary">
                  {organization.status}
                </Badge>
              )}
            </div>
          </div>
        </div>

        {/* =====================================================================
         * Contact
         * ===================================================================== */}

        <section className="space-y-3">
          <h4 className="font-medium">
            Contact Information
          </h4>

          <div className="grid gap-4 sm:grid-cols-2">
            <DetailItem
              icon={
                <Mail className="h-4 w-4" />
              }
              label="Email"
              value={
                organization.email || "-"
              }
            />

            <DetailItem
              icon={
                <Mail className="h-4 w-4" />
              }
              label="Support Email"
              value={
                organization.supportEmail ||
                "-"
              }
            />

            <DetailItem
              icon={
                <Phone className="h-4 w-4" />
              }
              label="Phone"
              value={
                organization.phone || "-"
              }
            />

            <DetailItem
              icon={
                <Globe className="h-4 w-4" />
              }
              label="Website"
              value={
                organization.website ||
                "-"
              }
            />
          </div>
        </section>

        {/* =====================================================================
         * Address
         * ===================================================================== */}

        <section className="space-y-3">
          <h4 className="font-medium">
            Address
          </h4>

          <div className="grid gap-4 sm:grid-cols-2">
            <DetailItem
              icon={
                <MapPin className="h-4 w-4" />
              }
              label="Address"
              value={
                organization.address ||
                "-"
              }
            />

            <DetailItem
              icon={
                <MapPin className="h-4 w-4" />
              }
              label="City"
              value={
                organization.city || "-"
              }
            />

            <DetailItem
              icon={
                <MapPin className="h-4 w-4" />
              }
              label="State"
              value={
                organization.state || "-"
              }
            />

            <DetailItem
              icon={
                <MapPin className="h-4 w-4" />
              }
              label="Country"
              value={
                organization.country ||
                "-"
              }
            />

            <DetailItem
              icon={
                <MapPin className="h-4 w-4" />
              }
              label="Postal Code"
              value={
                organization.postalCode ||
                "-"
              }
            />

            <DetailItem
              icon={
                <MapPin className="h-4 w-4" />
              }
              label="Timezone"
              value={
                organization.timezone ||
                "-"
              }
            />
          </div>
        </section>

        {/* =====================================================================
         * Organization Information
         * ===================================================================== */}

        <section className="space-y-3">
          <h4 className="font-medium">
            Organization Information
          </h4>

          <div className="grid gap-4 sm:grid-cols-2">
            <DetailItem
              label="Organization ID"
              value={organization.id}
            />

            <DetailItem
              label="Slug"
              value={
                organization.slug || "-"
              }
            />

            <DetailItem
              label="Size"
              value={
                organization.size || "-"
              }
            />

            <DetailItem
              label="Verification Status"
              value={
                organization.verificationStatus ||
                "-"
              }
            />

            <DetailItem
              label="Demo Organization"
              value={
                organization.isDemo
                  ? "Yes"
                  : "No"
              }
            />
          </div>
        </section>

        {/* =====================================================================
         * Legal Information
         * ===================================================================== */}

        <section className="space-y-3">
          <h4 className="font-medium">
            Legal & Compliance
          </h4>

          <div className="grid gap-4 sm:grid-cols-2">
            <DetailItem
              label="Registration Number"
              value={
                organization.registrationNumber ||
                "-"
              }
            />

            <DetailItem
              label="Tax Number"
              value={
                organization.taxNumber ||
                "-"
              }
            />

            <DetailItem
              label="License Number"
              value={
                organization.licenseNumber ||
                "-"
              }
            />

            <DetailItem
              label="Accreditation"
              value={
                organization.accreditation ||
                "-"
              }
            />
          </div>
        </section>

        {/* =====================================================================
         * Description
         * ===================================================================== */}

        {organization.description && (
          <section className="space-y-3">
            <h4 className="font-medium">
              Description
            </h4>

            <p className="text-sm leading-6 text-muted-foreground">
              {organization.description}
            </p>
          </section>
        )}

        {/* =====================================================================
         * Audit Information
         * ===================================================================== */}

        <section className="space-y-3">
          <h4 className="font-medium">
            Record Information
          </h4>

          <div className="grid gap-4 sm:grid-cols-2">
            <DetailItem
              label="Created"
              value={
                organization.createdAt ||
                "-"
              }
            />

            <DetailItem
              label="Last Updated"
              value={
                organization.updatedAt ||
                "-"
              }
            />
          </div>
        </section>
      </div>
    </EntityDialog>
  );
}

/* =============================================================================
 * Detail Item
 * =============================================================================
 */

type DetailItemProps =
  Readonly<{
    icon?: ReactNode;

    label: string;

    value: string;
  }>;

function DetailItem({
  icon,
  label,
  value,
}: DetailItemProps) {
  return (
    <div className="space-y-1">
      <div className="flex items-center gap-2 text-xs font-medium text-muted-foreground">
        {icon}

        <span>
          {label}
        </span>
      </div>

      <div className="text-sm">
        {value}
      </div>
    </div>
  );
}
