"use client";

import type { ReactNode } from "react";

import { useDatavionRuntime } from "./runtime-provider";

export function DatavionRuntimeGuard({
  children,
  module,
  role,
  permission,
  department,
}: {
  children: ReactNode;
  module?: string;
  role?: string;
  permission?: string;
  department?: string;
}) {
  const runtime = useDatavionRuntime();

  if (runtime.loading) {
    return null;
  }

  if (!runtime.authenticated) {
    return null;
  }

  if (
    module &&
    runtime.effective?.modules?.[module] !== true
  ) {
    return null;
  }

  if (
    role &&
    !runtime.effective?.roles?.includes(role)
  ) {
    return null;
  }

  if (
    permission &&
    !runtime.effective?.permissions?.includes(permission)
  ) {
    return null;
  }

  if (
    department &&
    !runtime.effective?.departments?.includes(department)
  ) {
    return null;
  }

  return <>{children}</>;
}
