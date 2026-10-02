import type {
  EffectiveCapabilityContext,
} from "../types/capability";

import type {
  RuntimeNavigationItem,
} from "../types/navigation";

import {
  hasCapability,
  hasModule,
  hasPermission,
} from "./capability";

const NAVIGATION: RuntimeNavigationItem[] = [
  {
    id: "dashboard",
    label: "Dashboard",
    href: "/dashboard",
  },
  {
    id: "patients",
    label: "Patients",
    href: "/patients",
    requiredModule: "patient_management",
  },
  {
    id: "appointments",
    label: "Appointments",
    href: "/appointments",
    requiredModule: "appointments",
  },
  {
    id: "pharmacy",
    label: "Pharmacy",
    href: "/pharmacy",
    requiredModule: "pharmacy",
  },
  {
    id: "laboratory",
    label: "Laboratory",
    href: "/laboratory",
    requiredModule: "laboratory",
  },
  {
    id: "imaging",
    label: "Imaging",
    href: "/imaging",
    requiredModule: "imaging",
  },
  {
    id: "billing",
    label: "Billing",
    href: "/billing",
    requiredModule: "billing",
  },
  {
    id: "telemedicine",
    label: "Telemedicine",
    href: "/telemedicine",
    requiredModule: "telemedicine",
  },
];

function visible(
  item: RuntimeNavigationItem,
  context: EffectiveCapabilityContext,
): boolean {
  if (
    item.requiredModule &&
    !hasModule(context, item.requiredModule)
  ) {
    return false;
  }

  if (
    item.requiredCapability &&
    !hasCapability(context, item.requiredCapability)
  ) {
    return false;
  }

  if (
    item.requiredPermission &&
    !hasPermission(context, item.requiredPermission)
  ) {
    return false;
  }

  return true;
}

export function resolveRuntimeNavigation(
  context: EffectiveCapabilityContext,
): RuntimeNavigationItem[] {
  return NAVIGATION
    .filter((item) => visible(item, context))
    .map((item) => ({
      ...item,
      children: item.children
        ?.filter((child) => visible(child, context)),
    }));
}

/**
 * Resolve visible navigation entries against the effective
 * capability context.
 */
export function resolveNavigation<T>(
  items: readonly T[],
  isAllowed: (item: T) => boolean,
): T[] {
  return items.filter(isAllowed);
}
