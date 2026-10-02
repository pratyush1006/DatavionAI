"use client";

function datavionRuntimeNavigationAllowed(
  runtimeCapability: {
    modules?: Record<string, boolean>;
    features?: Record<string, boolean>;
    permissions?: string[];
  } | null,
  item: {
    moduleKey?: string;
    featureKey?: string;
    permission?: string;
  },
): boolean {
  if (!runtimeCapability) {
    return false;
  }

  if (
    item.moduleKey &&
    runtimeCapability.modules &&
    runtimeCapability.modules[item.moduleKey] === false
  ) {
    return false;
  }

  if (
    item.featureKey &&
    runtimeCapability.features &&
    runtimeCapability.features[item.featureKey] === false
  ) {
    return false;
  }

  if (
    item.permission &&
    runtimeCapability.permissions &&
    !runtimeCapability.permissions.includes(item.permission)
  ) {
    return false;
  }

  return true;
}

/**
 * DatavionOS backend-driven application sidebar.
 *
 * Backend bootstrap is authoritative for navigation. No frontend
 * entitlement, subscription, RBAC, department or AI access decision is made
 * in this component.
 */


import { useMemo } from "react";

import { useBootstrap } from "@/core/bootstrap";
import {
  adaptBootstrapNavigation,
  SIDEBAR_GROUPS,
} from "@/core/navigation";

import { AppLogo } from "./app-logo";
import { SidebarGroup } from "./sidebar-group";
import { SidebarItem } from "./sidebar-item";
import { useRuntimeCapability } from "./../../datavionos/runtime/components/RuntimeShellProvider";

export function AppSidebar() {
  const runtimeCapability = useRuntimeCapability();
  const {
    bootstrap,
    isLoading,
    isFetching,
    isError,
  } = useBootstrap();

  const navigation = useMemo(() => {
    if (bootstrap === null) {
      return [];
    }

    return adaptBootstrapNavigation({
      navigation: bootstrap.navigation,
      modules: bootstrap.modules,
      portal: "staff",
    });
  }, [bootstrap]);

  const showLoading = isLoading && bootstrap === null;
  const showError = isError && bootstrap === null;
  const showUpdating =
    isFetching &&
    !isLoading &&
    bootstrap !== null;
  const showEmpty =
    bootstrap !== null &&
    !isLoading &&
    !isError &&
    navigation.length === 0;

  return (
    <aside className="d-flex h-screen w-72 flex-column border-end bg-body">
      <div className="border-bottom p-4">
        <AppLogo />
      </div>

      <nav
        aria-label="Primary navigation"
        className="flex-grow-1 overflow-y-auto p-3"
      >
        {showLoading ? (
          <div className="px-2 py-3 small text-body-secondary">
            Loading navigation...
          </div>
        ) : null}

        {showError ? (
          <div
            role="alert"
            className="alert alert-danger py-2 px-3 mb-2 small"
          >
            Unable to load navigation.
          </div>
        ) : null}

        {showUpdating ? (
          <div
            role="status"
            aria-live="polite"
            className="px-2 pb-2 small text-body-secondary"
          >
            Updating workspace...
          </div>
        ) : null}

        {bootstrap !== null
          ? SIDEBAR_GROUPS.map((group) => {
              const items = navigation.filter(
                (item) => item.group === group,
              );

              if (items.length === 0) {
                return null;
              }

              return (
                <SidebarGroup
                  key={group}
                  title={group}
                >
                  {items.map((item) => (
                    <SidebarItem
                      key={item.id}
                      item={item}
                    />
                  ))}
                </SidebarGroup>
              );
            })
          : null}

        {showEmpty ? (
          <div className="px-2 py-3 small text-body-secondary">
            {navigation.length === 0 ? "No navigation items are available for this workspace." : null}
          </div>
        ) : null}
      </nav>
    </aside>
  );
}

export default AppSidebar;
