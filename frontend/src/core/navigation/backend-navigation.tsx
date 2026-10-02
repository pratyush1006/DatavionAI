"use client";

import Link from "next/link";

import { DATAVION_RUNTIME_MODULES } from "../runtime/runtime-module-registry";
import { buildBackendNavigation } from "./backend-navigation";
import { useDatavionRuntime } from "../runtime/runtime-provider";

export interface BackendNavigationItem {
  key: string;
  label: string;
  path: string;
  visible: boolean;
  roles?: string[];
  permissions?: string[];
  departments?: string[];
}

function allowed(
  item: BackendNavigationItem,
  runtime: ReturnType<typeof useDatavionRuntime>,
): boolean {
  const effective = runtime.effective;

  if (!effective) {
    return false;
  }

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
}

export function getBackendNavigation(
  runtime: ReturnType<typeof useDatavionRuntime>,
): BackendNavigationItem[] {
  const effective = runtime.effective;

  if (!effective) {
    return [];
  }

  const items = DATAVION_RUNTIME_MODULES.map((module) => ({
    key: module.key,
    label: module.label,
    path: module.path,
    visible: effective.modules[module.key] === true,
    roles: [],
    permissions: [],
    departments: [],
  }));

  return buildBackendNavigation(items, runtime);
}

export function BackendNavigation() {
  const runtime = useDatavionRuntime();

  if (runtime.loading || !runtime.authenticated) {
    return null;
  }

  const navigation = getBackendNavigation(runtime);

  return (
    <nav aria-label="DatavionOS navigation">
      {navigation.map((item) => (
        <Link
          href={item.path}
          key={item.key}
          className="nav-link"
        >
          {item.label}
        </Link>
      ))}
    </nav>
  );
}
