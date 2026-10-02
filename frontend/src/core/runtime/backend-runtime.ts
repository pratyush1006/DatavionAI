/**
 * DatavionOS backend-authoritative runtime consumer.
 *
 * The backend owns SaaS entitlements, organization controls, RBAC,
 * department/data scope, AI scope, navigation visibility, and dashboard
 * composition. This module only adapts and renders that resolved contract.
 */

"use client";

import { useBootstrap } from "@/core/bootstrap";
import { adaptBootstrapNavigation } from "@/core/navigation";
import type { NavigationItem } from "@/core/navigation";

export interface BackendRuntime {
  readonly navigation: readonly NavigationItem[];
  readonly dashboard: ReturnType<typeof useBootstrap>["bootstrap"] extends infer T
    ? T extends { dashboard: infer D } ? D : never
    : never;
  readonly organizationName: string;
  readonly tenantName: string;
  readonly userName: string;
  readonly subscriptionName: string | null;
  readonly subscriptionStatus: string | null;
  readonly isLoading: boolean;
  readonly isFetching: boolean;
  readonly isError: boolean;
  readonly error: Error | null;
  readonly refetch: () => Promise<unknown>;
}

function displayName(
  firstName?: string,
  lastName?: string,
  fullName?: string,
): string {
  const full = fullName?.trim();
  if (full) return full;
  return [firstName, lastName].filter(Boolean).join(" ").trim();
}

export function useBackendRuntime(): BackendRuntime {
  const runtime = useBootstrap();
  const bootstrap = runtime.bootstrap;

  if (!bootstrap) {
    return {
      navigation: [],
      dashboard: [],
      organizationName: "",
      tenantName: "",
      userName: "",
      subscriptionName: null,
      subscriptionStatus: null,
      isLoading: runtime.isLoading,
      isFetching: runtime.isFetching,
      isError: runtime.isError,
      error: runtime.error,
      refetch: runtime.refetch,
    };
  }

  return {
    navigation: adaptBootstrapNavigation({
      navigation: bootstrap.navigation,
      modules: bootstrap.modules,
      portal: "staff",
    }),
    dashboard: bootstrap.dashboard,
    organizationName: bootstrap.organization?.name ?? "",
    tenantName: bootstrap.tenant?.name ?? "",
    userName:
      displayName(
        bootstrap.user.first_name,
        bootstrap.user.last_name,
        bootstrap.user.full_name,
      ) ||
      bootstrap.user.username ||
      bootstrap.user.email ||
      "User",
    subscriptionName: bootstrap.subscription?.plan?.name ?? null,
    subscriptionStatus: bootstrap.subscription?.status ?? null,
    isLoading: runtime.isLoading,
    isFetching: runtime.isFetching,
    isError: runtime.isError,
    error: runtime.error,
    refetch: runtime.refetch,
  };
}
