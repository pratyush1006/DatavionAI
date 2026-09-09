/**
 * =============================================================================
 * DatavionOS
 * File: src/core/navigation/navigation.adapter.ts
 * =============================================================================
 *
 * Adapter between the backend platform bootstrap contract and the frontend
 * navigation presentation contract.
 *
 * Backend is authoritative for:
 *
 * - available modules
 * - effective permissions
 * - navigation visibility
 * - navigation ordering
 * - routes
 * - navigation metadata
 *
 * Frontend is responsible for:
 *
 * - Lucide icon components
 * - frontend presentation groups
 * - portal presentation
 * - adapting backend runtime data to the frontend UI contract
 *
 * Unknown or invalid backend navigation data is intentionally rejected
 * instead of being silently mapped to an arbitrary UI location.
 *
 * =============================================================================
 */

import type {
  BootstrapModule,
  BootstrapNavigationItem,
} from "@/core/bootstrap";

import {
  NavigationIcons,
} from "./navigation.icons";

import type {
  NavigationItem,
} from "./navigation.types";

/* =============================================================================
 * Constants
 * =============================================================================
 */

/**
 * Runtime portal used by the staff application shell.
 */
const STAFF_PORTAL = "staff" as const;

/**
 * Map backend navigation categories to frontend sidebar groups.
 *
 * Backend categories and frontend groups are deliberately kept separate
 * because they represent different contracts.
 */
const CATEGORY_TO_GROUP: Readonly<
  Record<
    string,
    NavigationItem["group"]
  >
> = {
  dashboard: "dashboard",
  clinical: "clinical",
  diagnostics: "diagnostics",
  operations: "operations",
  ai: "ai",
  reports: "reports",
  administration: "administration",
};

/* =============================================================================
 * Helpers
 * =============================================================================
 */

/**
 * Normalize runtime identifiers before comparison.
 */
function normalize(
  value: unknown,
): string {
  if (
    value === null ||
    value === undefined
  ) {
    return "";
  }

  return String(value)
    .trim()
    .toLowerCase();
}

/**
 * Resolve a backend navigation category into a frontend sidebar group.
 *
 * Unknown categories fail closed.
 */
function resolveGroup(
  category: string,
): NavigationItem["group"] | null {
  return (
    CATEGORY_TO_GROUP[
      normalize(category)
    ] ?? null
  );
}

/**
 * Resolve a backend icon identifier to a registered Lucide icon.
 *
 * Resolution priority:
 *
 * 1. Backend module identifier
 * 2. Backend navigation icon identifier
 *
 * Unknown icons fail closed rather than silently displaying an unrelated icon.
 */
function resolveIcon(
  identifier: string,
  iconName: string,
): NavigationItem["icon"] | null {
  const normalizedIdentifier =
    normalize(identifier);

  const normalizedIcon =
    normalize(iconName);

  if (
    normalizedIdentifier in
    NavigationIcons
  ) {
    return NavigationIcons[
      normalizedIdentifier as keyof typeof NavigationIcons
    ];
  }

  if (
    normalizedIcon in
    NavigationIcons
  ) {
    return NavigationIcons[
      normalizedIcon as keyof typeof NavigationIcons
    ];
  }

  return null;
}

/* =============================================================================
 * Adapter Options
 * =============================================================================
 */

export interface NavigationAdapterOptions {
  /**
   * Backend-resolved navigation items.
   */
  readonly navigation:
    readonly BootstrapNavigationItem[];

  /**
   * Backend-resolved runtime modules.
   *
   * Modules provide the canonical module identifier used by the frontend
   * navigation contract.
   */
  readonly modules:
    readonly BootstrapModule[];

  /**
   * Frontend presentation portal.
   *
   * Defaults to the staff application portal.
   */
  readonly portal?:
    NavigationItem["portals"][number];
}

/* =============================================================================
 * Adapter
 * =============================================================================
 */

/**
 * Adapt backend-resolved navigation into the frontend presentation contract.
 *
 * The backend remains authoritative for:
 *
 * - navigation visibility
 * - effective permissions
 * - navigation ordering
 * - routes
 * - runtime module availability
 *
 * The adapter performs only structural translation required by the frontend.
 *
 * Invalid navigation entries are omitted:
 *
 * - missing matching module
 * - unknown category
 * - unknown icon
 *
 * This provides fail-closed behavior for the application shell.
 */
export function adaptBootstrapNavigation({
  navigation,
  modules,
  portal = STAFF_PORTAL,
}: NavigationAdapterOptions): NavigationItem[] {
  /**
   * Index runtime modules by normalized route.
   *
   * The backend navigation contract currently identifies the corresponding
   * runtime module through the route, so route is used as the join key.
   */
  const modulesByRoute =
    new Map<
      string,
      BootstrapModule
    >();

  for (
    const runtimeModule of modules
  ) {
    const route =
      normalize(
        runtimeModule.route,
      );

    if (!route) {
      continue;
    }

    modulesByRoute.set(
      route,
      runtimeModule,
    );
  }

  /**
   * Preserve backend ordering.
   *
   * Route is used only as a deterministic tie-breaker.
   */
  return [...navigation]
    .sort(
      (
        left,
        right,
      ) =>
        left.order -
          right.order ||
        left.route.localeCompare(
          right.route,
        ),
    )
    .flatMap(
      (
        item,
      ) => {
        /**
         * Navigation must correspond to a registered runtime module.
         */
        const runtimeModule =
          modulesByRoute.get(
            normalize(
              item.route,
            ),
          );

        if (!runtimeModule) {
          return [];
        }

        /**
         * Resolve frontend presentation group.
         *
         * Unknown backend categories are rejected.
         */
        const group =
          resolveGroup(
            item.category,
          );

        if (!group) {
          return [];
        }

        /**
         * Resolve the icon from the controlled frontend icon registry.
         *
         * Module identifiers are preferred because they provide a stable
         * runtime identity.
         *
         * Backend icon metadata remains a supported fallback.
         */
        const icon =
          resolveIcon(
            runtimeModule.identifier,
            item.icon,
          );

        if (!icon) {
          return [];
        }

        /**
         * Backend is authoritative for effective navigation permissions.
         *
         * Empty permission identifiers are discarded because they have no
         * meaningful frontend representation.
         */
        const permissions =
          item.permissions.filter(
            (
              permission,
            ) =>
              normalize(
                permission,
              ).length > 0,
          );

        return [
          {
            id:
              runtimeModule.identifier,

            label:
              item.title,

            href:
              item.route,

            icon,

            group,

            module:
              runtimeModule.identifier,

            permissions,

            portals: [
              portal,
            ],
          },
        ];
      },
    );
}

/* =============================================================================
 * Public API
 * =============================================================================
 */

export default adaptBootstrapNavigation;
