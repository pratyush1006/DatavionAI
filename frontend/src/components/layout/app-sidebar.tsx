/**
 * =============================================================================
 * DatavionOS
 * File: src/components/layout/app-sidebar.tsx
 * =============================================================================
 *
 * Enterprise application sidebar.
 *
 * Runtime navigation is resolved from the backend platform bootstrap.
 *
 * Backend is authoritative for:
 *
 * - enabled modules
 * - effective permissions
 * - navigation visibility
 * - navigation ordering
 * - tenant context
 * - organization context
 *
 * The navigation adapter translates the backend runtime contract into the
 * frontend navigation presentation contract.
 *
 * =============================================================================
 */

"use client";

import { useMemo } from "react";

import { useBootstrap } from "@/core/bootstrap";

import {
  adaptBootstrapNavigation,
  SIDEBAR_GROUPS,
} from "@/core/navigation";

import { AppLogo } from "./app-logo";
import { SidebarGroup } from "./sidebar-group";
import { SidebarItem } from "./sidebar-item";

/**
 * Enterprise application sidebar.
 */
export function AppSidebar() {
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

  const showLoading =
    isLoading && bootstrap === null;

  const showError =
    isError && bootstrap === null;

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
    <aside className="flex h-screen w-72 flex-col border-r bg-background">
      <div className="border-b p-6">
        <AppLogo />
      </div>

      <nav
        aria-label="Primary navigation"
        className="flex-1 overflow-y-auto p-4"
      >
        {showLoading ? (
          <div className="px-2 py-3 text-sm text-muted-foreground">
            Loading navigation...
          </div>
        ) : null}

        {showError ? (
          <div
            role="alert"
            className="px-2 py-3 text-sm text-destructive"
          >
            Unable to load navigation.
          </div>
        ) : null}

        {showUpdating ? (
          <div
            role="status"
            aria-live="polite"
            className="px-2 pb-2 text-xs text-muted-foreground"
          >
            Updating...
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
          <div className="px-2 py-3 text-sm text-muted-foreground">
            No navigation items are available.
          </div>
        ) : null}
      </nav>
    </aside>
  );
}

export default AppSidebar;
