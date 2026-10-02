export interface BackendNavigationItem {
  key: string;
  label: string;
  path: string;
  visible: boolean;
  roles?: string[];
  permissions?: string[];
  departments?: string[];
}

export function filterBackendNavigation(
  items: BackendNavigationItem[],
  effective: {
    modules: Record<string, boolean>;
    roles: string[];
    permissions: string[];
    departments: string[];
  },
): BackendNavigationItem[] {
  return items.filter((item) => {
    if (effective.modules[item.key] !== true) {
      return false;
    }

    if (
      item.roles?.length &&
      !item.roles.some((role) => effective.roles.includes(role))
    ) {
      return false;
    }

    if (
      item.permissions?.length &&
      !item.permissions.some((permission) =>
        effective.permissions.includes(permission),
      )
    ) {
      return false;
    }

    if (
      item.departments?.length &&
      !item.departments.some((department) =>
        effective.departments.includes(department),
      )
    ) {
      return false;
    }

    return true;
  });
}
