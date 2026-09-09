/**
 * =============================================================================
 * DatavionOS
 * File: src/core/navigation/navigation.config.ts
 * =============================================================================
 *
 * Frontend navigation implementation registry.
 *
 * The backend remains authoritative for:
 *
 * - runtime module availability
 * - effective permissions
 * - navigation visibility
 * - navigation ordering
 * - backend navigation metadata
 *
 * This configuration is responsible only for frontend presentation and
 * implemented application routes.
 *
 * A backend runtime module is rendered in the sidebar only when a corresponding
 * frontend implementation is registered here.
 *
 * This provides intentional fail-closed behavior:
 *
 *     Backend module
 *          |
 *          v
 *     Frontend registry
 *          |
 *       implemented?
 *        /       \
 *      yes       no
 *       |         |
 *       v         v
 *    render     omit
 *
 * =============================================================================
 */

import {
  NavigationIcons,
} from "./navigation.icons";

import type {
  NavigationItem,
} from "./navigation.types";

/* =============================================================================
 * Navigation Configuration
 * =============================================================================
 *
 * Only frontend routes that are actually implemented should be registered.
 *
 * IMPORTANT:
 *
 * The `module` value must match the backend runtime module identifier.
 *
 * Backend:
 *
 *     appointment-management
 *
 * Frontend:
 *
 *     /appointments
 *
 * The route does not need to be identical to the backend route.
 *
 * =============================================================================
 */

export const NAVIGATION_CONFIG: NavigationItem[] = [
  /* ===========================================================================
   * Dashboard
   * ===========================================================================
   */

  {
    id: "dashboard",

    label: "Dashboard",

    href: "/dashboard",

    icon:
      NavigationIcons.dashboard,

    group: "dashboard",

    module: "dashboard",

    permissions: [
      "dashboard.view",
    ],

    portals: [
      "staff",
    ],
  },

  /* ===========================================================================
   * Patients
   * ===========================================================================
   */

  {
    id: "patients",

    label: "Patients",

    href: "/patients",

    icon:
      NavigationIcons.patients,

    group: "clinical",

    module: "patients",

    permissions: [
      "patient.view",
    ],

    portals: [
      "staff",
    ],
  },

  /* ===========================================================================
   * Appointments
   * ===========================================================================
   *
   * Backend runtime module:
   *
   *     appointment-management
   *
   * Backend runtime route:
   *
   *     /clinical/appointments
   *
   * Implemented frontend route:
   *
   *     /appointments
   *
   * The adapter intentionally maps the backend runtime module to the
   * implemented frontend route.
   * ===========================================================================
   */

  {
    id: "appointments",

    label: "Appointments",

    href: "/appointments",

    icon:
      NavigationIcons.appointments,

    group: "clinical",

    module: "appointment-management",

    permissions: [
      "appointment.view",
    ],

    portals: [
      "staff",
    ],
  },

  /* ===========================================================================
   * Organizations
   * ===========================================================================
   */

  {
    id: "organizations",

    label: "Organizations",

    href: "/organizations",

    icon:
      NavigationIcons.organizations,

    group: "administration",

    module: "organizations",

    permissions: [
      "organization.view",
    ],

    portals: [
      "staff",
    ],
  },
];

/* =============================================================================
 * Public API
 * =============================================================================
 */

export default NAVIGATION_CONFIG;
