/**
 * =============================================================================
 * DatavionOS
 * File: src/core/navigation/navigation.types.ts
 * =============================================================================
 *
 * Frontend navigation presentation contracts.
 *
 * The backend remains authoritative for runtime navigation visibility,
 * permissions, routes, ordering, and module availability.
 *
 * This file defines only the frontend presentation model.
 *
 * =============================================================================
 */

import type { LucideIcon } from "lucide-react";

/* =============================================================================
 * Portal
 * =============================================================================
 */

export type NavigationPortal =
  | "staff"
  | "patient"
  | "organization"
  | "platform";

/* =============================================================================
 * Navigation Group
 * =============================================================================
 *
 * These are frontend presentation groups.
 *
 * Backend categories are adapted into these groups by:
 *
 *     @/core/navigation/navigation.adapter
 *
 * =============================================================================
 */

export type NavigationGroup =
  | "dashboard"
  | "clinical"
  | "diagnostics"
  | "operations"
  | "ai"
  | "reports"
  | "administration";

/* =============================================================================
 * Navigation Item
 * =============================================================================
 */

export interface NavigationItem {
  /**
   * Stable frontend navigation identifier.
   */
  readonly id: string;

  /**
   * User-facing navigation label.
   */
  readonly label: string;

  /**
   * Frontend application route.
   */
  readonly href: string;

  /**
   * Resolved Lucide icon component.
   */
  readonly icon: LucideIcon;

  /**
   * Frontend presentation group.
   */
  readonly group: NavigationGroup;

  /**
   * Canonical runtime module identifier.
   */
  readonly module: string;

  /**
   * Effective permissions supplied by the backend.
   */
  readonly permissions: string[];

  /**
   * Application portals where this item is presented.
   */
  readonly portals: NavigationPortal[];

  /**
   * Optional nested navigation items.
   */
  readonly children?: NavigationItem[];
}
