"use client";

import { useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";

import { authRuntime } from "@/core/auth";
import { BOOTSTRAP_QUERY_KEY } from "@/core/bootstrap";
import type { PlatformBootstrap } from "@/core/bootstrap";
import { fetchMyTenants, selectTenant } from "@/core/tenancy/service";
import { useBootstrap } from "@/core/bootstrap";

const TENANTS_QUERY_KEY = ["tenancy", "my-tenants"] as const;

export function TenantSwitcher() {
  const queryClient = useQueryClient();
  const { bootstrap } = useBootstrap();
  const [isSelecting, setIsSelecting] = useState(false);
  const [selectionError, setSelectionError] = useState("");
  const tenantsQuery = useQuery({
    queryKey: TENANTS_QUERY_KEY,
    queryFn: fetchMyTenants,
  });

  const tenants = tenantsQuery.data ?? [];
  const activeTenantId =
    bootstrap?.tenant?.id ?? authRuntime.userStorage.getTenantId() ?? "";

  async function handleTenantChange(tenantId: string) {
    if (!tenantId || tenantId === activeTenantId) {
      return;
    }

    setIsSelecting(true);
    setSelectionError("");

    try {
      await selectTenant(tenantId);
      const user = authRuntime.userStorage.getUser();
      if (user) {
        authRuntime.userStorage.updateUser({
          tenantId,
          organizationId: null,
        });
      }
      await queryClient.invalidateQueries({ queryKey: BOOTSTRAP_QUERY_KEY });
      const nextBootstrap = queryClient.getQueryData<PlatformBootstrap>(
        BOOTSTRAP_QUERY_KEY,
      );
      if (user && nextBootstrap) {
        authRuntime.userStorage.updateUser({
          organizationId: nextBootstrap.organization?.id ?? null,
        });
      }
    } catch (reason) {
      setSelectionError(
        reason instanceof Error
          ? reason.message
          : "Unable to switch workspace. Please try again.",
      );
    } finally {
      setIsSelecting(false);
    }
  }

  if (!tenantsQuery.data?.length) {
    return null;
  }

  return (
    <div className="d-flex flex-column align-items-start">
      <label className="visually-hidden" htmlFor="active-tenant">
        Active workspace
      </label>
      <select
        id="active-tenant"
        aria-label="Active workspace"
        data-testid="tenant-switcher"
        className="form-select form-select-sm w-auto"
        value={activeTenantId}
        disabled={isSelecting || tenantsQuery.isLoading || tenants.length < 2}
        onChange={(event) => void handleTenantChange(event.target.value)}
      >
        {tenants.map((tenant) => (
          <option key={tenant.id} value={tenant.id}>
            {tenant.name}
          </option>
        ))}
      </select>
      {selectionError ? (
        <span className="small text-danger mt-1" role="alert">
          {selectionError}
        </span>
      ) : null}
    </div>
  );
}
