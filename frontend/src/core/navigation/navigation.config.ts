/**
 * Navigation configuration.
 */

import { NavigationIcons } from "./navigation.icons";
import type { NavigationItem } from "./navigation.types";

export const NAVIGATION_CONFIG: NavigationItem[] = [
  {
    id: "dashboard",
    label: "Dashboard",
    href: "/dashboard",
    icon: NavigationIcons.dashboard,
    group: "dashboard",
    module: "dashboard",
    permissions: ["dashboard.view"],
    portals: ["staff"],
  },

  {
    id: "patients",
    label: "Patients",
    href: "/patients",
    icon: NavigationIcons.patients,
    group: "clinical",
    module: "patients",
    permissions: ["patient.view"],
    portals: ["staff"],
  },

  {
    id: "appointments",
    label: "Appointments",
    href: "/appointments",
    icon: NavigationIcons.appointments,
    group: "clinical",
    module: "appointments",
    permissions: ["appointment.view"],
    portals: ["staff"],
  },

  {
    id: "encounters",
    label: "Encounters",
    href: "/encounters",
    icon: NavigationIcons.encounters,
    group: "clinical",
    module: "encounters",
    permissions: ["encounter.view"],
    portals: ["staff"],
  },

  {
    id: "laboratories",
    label: "Laboratories",
    href: "/laboratories",
    icon: NavigationIcons.laboratories,
    group: "diagnostics",
    module: "laboratories",
    permissions: ["laboratory.view"],
    portals: ["staff"],
  },

  {
    id: "radiology",
    label: "Radiology",
    href: "/radiology",
    icon: NavigationIcons.radiology,
    group: "diagnostics",
    module: "radiology",
    permissions: ["radiology.view"],
    portals: ["staff"],
  },

  {
    id: "billing",
    label: "Billing",
    href: "/billing",
    icon: NavigationIcons.billing,
    group: "operations",
    module: "billing",
    permissions: ["billing.view"],
    portals: ["staff"],
  },
  {
  id: "organizations",
  label: "Organizations",
  href: "/organizations",
  icon: NavigationIcons.organizations,
  group: "administration",
  module: "organizations",
  permissions: ["organization.view"],
  portals: ["staff"],
},
  {
    id: "settings",
    label: "Settings",
    href: "/settings",
    icon: NavigationIcons.settings,
    group: "administration",
    module: "settings",
    permissions: ["settings.view"],
    portals: ["staff"],
  },
];
