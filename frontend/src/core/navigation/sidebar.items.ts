/**
 * =============================================================================
 * DatavionOS
 * File: src/core/navigation/sidebar.items.ts
 * =============================================================================
 *
 * Sidebar presentation group ordering.
 *
 * The list controls presentation order only.
 *
 * Runtime visibility and ordering of individual navigation items remain
 * authoritative from the backend bootstrap payload.
 *
 * =============================================================================
 */

export const SIDEBAR_GROUPS = [
  "dashboard",
  "clinical",
  "diagnostics",
  "operations",
  "ai",
  "reports",
  "administration",
] as const;
