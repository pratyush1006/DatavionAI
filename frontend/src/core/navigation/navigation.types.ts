/**
 * Navigation type definitions.
 */

import type { LucideIcon } from "lucide-react";

export type NavigationPortal =
  | "staff"
  | "patient"
  | "organization"
  | "platform";

export type NavigationGroup =
  | "dashboard"
  | "clinical"
  | "diagnostics"
  | "operations"
  | "reports"
  | "administration";

export interface NavigationItem {
  id: string;

  label: string;

  href: string;

  icon: LucideIcon;

  group: NavigationGroup;

  module: string;

  permissions: string[];

  portals: NavigationPortal[];

  children?: NavigationItem[];
}
