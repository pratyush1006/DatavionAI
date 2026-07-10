/**
 * Navigation builder.
 */

import { NAVIGATION_CONFIG } from "./navigation.config";
import type {
  NavigationItem,
  NavigationPortal,
} from "./navigation.types";

export interface NavigationBuilderOptions {
  portal: NavigationPortal;

  enabledModules: string[];

  permissions: string[];
}

export class NavigationBuilder {
  static build({
    portal,
    enabledModules,
    permissions,
  }: NavigationBuilderOptions): NavigationItem[] {
    return NAVIGATION_CONFIG.filter((item) => {
      const hasPortal = item.portals.includes(portal);

      const hasModule = enabledModules.includes(item.module);

      const hasPermission = item.permissions.every((permission) =>
        permissions.includes(permission),
      );

      return hasPortal && hasModule && hasPermission;
    });
  }
}
