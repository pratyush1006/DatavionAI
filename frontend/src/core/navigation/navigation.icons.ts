/**
 * =============================================================================
 * DatavionOS
 * File: src/core/navigation/navigation.icons.ts
 * =============================================================================
 *
 * Controlled frontend navigation icon registry.
 *
 * The backend may provide icon metadata, but executable Lucide components
 * remain a frontend responsibility.
 *
 * Runtime module identifiers are also registered here where they are used
 * directly by the navigation adapter.
 *
 * =============================================================================
 */

import {
  Activity,
  Bot,
  Building2,
  Calendar,
  ClipboardList,
  FlaskConical,
  Home,
  Receipt,
  Settings,
  Stethoscope,
  Users,
  Workflow,
} from "lucide-react";

/* =============================================================================
 * Navigation Icons
 * =============================================================================
 */

export const NavigationIcons = {
  /* ---------------------------------------------------------------------------
   * Core
   * ---------------------------------------------------------------------------
   */

  dashboard: Home,

  organizations: Building2,

  patients: Users,

  appointments: Calendar,

  encounters: ClipboardList,

  laboratories: FlaskConical,

  radiology: Stethoscope,

  billing: Receipt,

  settings: Settings,

  reports: Activity,

  /* ---------------------------------------------------------------------------
   * AI Platform
   * ---------------------------------------------------------------------------
   */

  "ai-assistant": Bot,

  "ai-workflow": Workflow,

  /* ---------------------------------------------------------------------------
   * Clinical Runtime Modules
   * ---------------------------------------------------------------------------
   */

  "appointment-management": Calendar,
} as const;
