/**
 * Organization details dialog.
 */

"use client";

import { useState } from "react";

import {
  Building2,
  Eye,
  Mail,
  MapPin,
  Phone,
} from "lucide-react";

import {
  EntityDialog,
} from "@/components/common/dialogs";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

import type {
  Organization,
} from "../../domain";

export type OrganizationDetailsProps =
  Readonly<{
    organization: Organization;
  }>;

export function OrganizationDetails({
  organization,
}: OrganizationDetailsProps) {
  const [open, setOpen] =
    useState(false);

  return (
    <>
      <Button
        variant="ghost"
        size="icon-sm"
        onClick={() =>
          setOpen(true)
        }
      >
        <Eye className="h-4 w-4" />

        <span className="sr-only">
          View organization
        </span>
      </Button>

      <EntityDialog
        open={open}
        onOpenChange={setOpen}
        title={organization.name}
        description="Organization details"
        size="lg"
      >
        <div className="space-y-6">
          <div className="flex items-center gap-4">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10">
              <Building2 className="h-6 w-6 text-primary" />
            </div>

            <div>
              <h3 className="text-lg font-semibold">
                {organization.name}
              </h3>

              <p className="text-sm text-muted-foreground">
                {organization.code}
              </p>
            </div>

            <div className="ml-auto">
              <Badge
                variant={
                  organization.isActive
                    ? "default"
                    : "destructive"
                }
              >
                {organization.isActive
                  ? "Active"
                  : "Inactive"}
              </Badge>
            </div>
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <div className="mb-1 text-sm font-medium">
                Organization Type
              </div>

              <Badge variant="secondary">
                {organization.organizationType.replaceAll(
                  "_",
                  " ",
                )}
              </Badge>
            </div>

            <div>
              <div className="mb-1 text-sm font-medium">
                Contact
              </div>

              <div className="space-y-2 text-sm">
                <div className="flex items-center gap-2">
                  <Mail className="h-4 w-4 text-muted-foreground" />
                  {organization.email || "-"}
                </div>

                <div className="flex items-center gap-2">
                  <Phone className="h-4 w-4 text-muted-foreground" />
                  {organization.phone || "-"}
                </div>
              </div>
            </div>

            <div className="md:col-span-2">
              <div className="mb-1 text-sm font-medium">
                Address
              </div>

              <div className="flex items-start gap-2 text-sm">
                <MapPin className="mt-0.5 h-4 w-4 text-muted-foreground" />

                <div>
                  <div>
                    {organization.address}
                  </div>

                  <div className="text-muted-foreground">
                    {organization.city},{" "}
                    {organization.state},{" "}
                    {organization.country}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </EntityDialog>
    </>
  );
}
