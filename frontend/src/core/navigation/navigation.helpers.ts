/**
 * Navigation helper functions.
 */

import type { NavigationItem } from "./navigation.types";

export function filterNavigation(
  items: NavigationItem[],
  permissions: string[],
): NavigationItem[] {
  return items.filter((item) =>
    item.permissions.every((permission) =>
      permissions.includes(permission),
    ),
  );
}
