/**
 * Navigation icons.
 */

import {
  Activity,
  Building2,
  Calendar,
  ClipboardList,
  FlaskConical,
  Home,
  Receipt,
  Settings,
  Stethoscope,
  Users,
} from "lucide-react";

export const NavigationIcons = {
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
} as const;
